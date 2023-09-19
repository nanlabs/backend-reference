//go:build integration

// integration package include logic related to todo api integration tests
package integration

import (
	"context"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"todo-api-golang/internal/config"

	"github.com/ory/dockertest/v3"
	"github.com/ory/dockertest/v3/docker"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

// IntegrationTest define the resources used to perform an integration tests
type IntegrationTest struct {
	pool     *dockertest.Pool
	network  *dockertest.Network
	config   *config.IntegrationConfig
	mongoRes *dockertest.Resource
	apiRes   *dockertest.Resource
}

// NewIntegrationTest creates the integration test resources.
func NewIntegrationTest(pool *dockertest.Pool, network *dockertest.Network, config *config.IntegrationConfig) *IntegrationTest {
	return &IntegrationTest{
		pool:    pool,
		network: network,
		config:  config,
	}
}

// Create a mongo db container to perform integrations tests.
func (i *IntegrationTest) StartMongoDB(mongoVersion string) error {
	r, err := i.pool.RunWithOptions(&dockertest.RunOptions{
		Name:         i.config.MongoHost,
		Repository:   "mongo",
		Tag:          mongoVersion,
		Networks:     []*dockertest.Network{i.network},
		ExposedPorts: []string{"27017"},
		PortBindings: map[docker.Port][]docker.PortBinding{
			docker.Port("27017"): {
				{HostIP: "localhost", HostPort: i.config.MongoPort},
			},
		},
		Env: []string{
			fmt.Sprintf("MONGO_INITDB_ROOT_USERNAME=%s", i.config.MongoUsername),
			fmt.Sprintf("MONGO_INITDB_ROOT_PASSWORD=%s", i.config.MongoPassword),
		},
	}, func(config *docker.HostConfig) {
		// set AutoRemove to true so that stopped container goes away by itself
		config.AutoRemove = true
		config.RestartPolicy = docker.RestartPolicy{
			Name: "no",
		}
	})
	if err != nil {
		log.Printf("Could not start Mongodb: %v \n", err)
		return err
	}

	err = r.Expire(60)
	if err != nil {
		log.Printf("Could set expiration time: %v \n", err)
	}

	mongoPort := r.GetPort("27017/tcp")

	log.Printf("mongo-%s - connecting to : %s \n", mongoVersion, fmt.Sprintf("mongodb://localhost:%s", mongoPort))
	if err := i.pool.Retry(func() error {
		var err error

		url := fmt.Sprintf("mongodb://%s:%s@localhost:%s", i.config.MongoUsername, i.config.MongoPassword, mongoPort)
		clientOptions := options.Client().ApplyURI(url)
		client, err := mongo.Connect(context.TODO(), clientOptions)
		if err != nil {
			return err
		}

		err = client.Ping(context.TODO(), nil)
		if err == nil {
			log.Println("successfully connected to Mongodb.")
			return nil
		}

		log.Printf("Retry connection to mongodb")
		return err

	}); err != nil {
		log.Printf("Could not connect to mongodb container: %v \n", err)
		return err
	}

	return nil
}

// Create a todo api container to perform integrations tests.
func (i *IntegrationTest) StartTodoAPI() (string, error) {
	apiContainerName := "todointegrationtest"

	r, err := i.pool.BuildAndRunWithBuildOptions(
		&dockertest.BuildOptions{
			ContextDir: "../../",
			Dockerfile: "./docker/todo/Dockerfile",
		},
		&dockertest.RunOptions{
			Name:         apiContainerName,
			Repository:   apiContainerName,
			Networks:     []*dockertest.Network{i.network},
			ExposedPorts: []string{i.config.HTTPServerPort},
			PortBindings: map[docker.Port][]docker.PortBinding{
				docker.Port(i.config.HTTPServerPort): {
					{HostIP: "localhost", HostPort: i.config.HTTPServerPort},
				},
			},
			Env: []string{
				fmt.Sprintf("HTTP_SERVER_HOST=%s", i.config.HTTPServerHost),
				fmt.Sprintf("HTTP_SERVER_PORT=%s", i.config.HTTPServerPort),
				fmt.Sprintf("HTTP_RATE_LIMIT=%f", i.config.HTTPRateLimit),
				fmt.Sprintf("HTTP_RATE_INTERVAL=%s", i.config.HTTPRateInterval),
				fmt.Sprintf("MONGO_USERNAME=%s", i.config.MongoUsername),
				fmt.Sprintf("MONGO_PASSWORD=%s", i.config.MongoPassword),
				fmt.Sprintf("MONGO_HOST=%s", i.config.MongoHost),
				fmt.Sprintf("MONGO_PORT=%s", "27017"),
				fmt.Sprintf("MONGO_DATABASE=%s", i.config.MongoDatabase),
				fmt.Sprintf("MONGO_COLLECTION=%s", i.config.MongoCollection),
			},
		}, func(config *docker.HostConfig) {
			// set AutoRemove to true so that stopped container goes away by itself
			config.AutoRemove = true
			config.RestartPolicy = docker.RestartPolicy{
				Name: "no",
			}
		})
	if err != nil {
		log.Printf("Could not start %s: %v \n", apiContainerName, err)
		return "", err
	}

	err = r.Expire(60)
	if err != nil {
		log.Printf("Could set expiration time: %v \n", err)
	}

	waiter, err := i.pool.Client.AttachToContainerNonBlocking(docker.AttachToContainerOptions{
		Container:    apiContainerName,
		OutputStream: log.Writer(),
		ErrorStream:  log.Writer(),
		RawTerminal:  true,
		Logs:         true,
		Stream:       true,
		Stdout:       true,
		Stderr:       true,
	})
	if err != nil {
		log.Println("Unable to attach logs to todo api container ", err)
	}
	defer waiter.Close()

	// appPort := r.GetPort("8082/tcp")
	appPort := r.GetPort(fmt.Sprintf("%s/tcp", i.config.HTTPServerPort))
	basePath := fmt.Sprintf("http://localhost:%s/api/v1", appPort)
	log.Printf("%s", basePath)
	if err := i.pool.Retry(func() error {

		resp, err := http.Get(fmt.Sprintf("%s/health", basePath))
		if err != nil {
			log.Printf("Trying to connect to %s on localhost:%s, got : %v \n", apiContainerName, appPort, err)
			return err
		}

		if resp.StatusCode != http.StatusOK {
			log.Printf("Trying to connect to %s on localhost:%s, got : %v , status: %v \n", apiContainerName, appPort, err, resp.StatusCode)
			return err
		}

		log.Println("Status: ", resp.StatusCode)
		rs, _ := io.ReadAll(resp.Body)
		log.Printf("Response: %s \n", rs)

		return nil
	}); err != nil {
		log.Printf("Could not connect to %s container: %v \n", apiContainerName, err)
		return "", err
	}
	return basePath, nil
}

// Remove integration tests containers.
func (i *IntegrationTest) CleanUp(code int) {
	fmt.Println("Removing resources.")
	if i.mongoRes != nil {
		if err := i.pool.Purge(i.mongoRes); err != nil {
			log.Fatalf("Could not purge resource: %s\n", err)
		}
	}

	if i.apiRes != nil {
		if err := i.pool.Purge(i.apiRes); err != nil {
			log.Fatalf("Could not purge resource: %s\n", err)
		}
	}

	if i.network != nil {
		if err := i.pool.RemoveNetwork(i.network); err != nil {
			log.Fatalf("Could not remove network: %s\n", err)
		}
	}
	os.Exit(code)
}
