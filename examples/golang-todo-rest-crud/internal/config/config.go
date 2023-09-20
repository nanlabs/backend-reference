// config package manages configuration variables of .env file and env variables.
package config

import (
	"github.com/spf13/viper"
)

// Config stores all configuration of the application.
// The values are read by viper from a config file or environment variable.
type Config struct {
	HTTPServerHost   string  `mapstructure:"HTTP_SERVER_HOST"`
	HTTPServerPort   string  `mapstructure:"HTTP_SERVER_PORT"`
	HTTPRateLimit    float64 `mapstructure:"HTTP_RATE_LIMIT"`
	HTTPRateInterval string  `mapstructure:"HTTP_RATE_INTERVAL"`
	MongoHost        string  `mapstructure:"MONGO_HOST"`
	MongoPort        string  `mapstructure:"MONGO_PORT"`
	MongoDatabase    string  `mapstructure:"MONGO_DATABASE"`
	MongoCollection  string  `mapstructure:"MONGO_COLLECTION"`
	MongoUsername    string  `mapstructure:"MONGO_USERNAME"`
	MongoPassword    string  `mapstructure:"MONGO_PASSWORD"`
}

// IntegrationConfig stores all configuration to run integration tests.
// The values are read by viper from a config file or environment variable.
type IntegrationConfig struct {
	HTTPServerHost   string  `mapstructure:"INTEGRATION_HTTP_SERVER_HOST"`
	HTTPServerPort   string  `mapstructure:"INTEGRATION_HTTP_SERVER_PORT"`
	HTTPRateLimit    float64 `mapstructure:"INTEGRATION_HTTP_RATE_LIMIT"`
	HTTPRateInterval string  `mapstructure:"INTEGRATION_HTTP_RATE_INTERVAL"`
	MongoHost        string  `mapstructure:"INTEGRATION_MONGO_HOST"`
	MongoPort        string  `mapstructure:"INTEGRATION_MONGO_PORT"`
	MongoDatabase    string  `mapstructure:"INTEGRATION_MONGO_DATABASE"`
	MongoCollection  string  `mapstructure:"INTEGRATION_MONGO_COLLECTION"`
	MongoUsername    string  `mapstructure:"INTEGRATION_MONGO_USERNAME"`
	MongoPassword    string  `mapstructure:"INTEGRATION_MONGO_PASSWORD"`
}

// LoadConfig set de default configuration type for the application.
func LoadConfig(path string) (*Config, error) {
	var config Config
	return loadConfig(path, config)
}

// LoadConfig set de default configuration type for the integration tests.
func LoadIntegrationConfig(path string) (*IntegrationConfig, error) {
	var config IntegrationConfig
	return loadConfig(path, config)
}

// loadConfig reads configuration from file or environment variables.
func loadConfig[T any](path string, config T) (*T, error) {
	viper.AddConfigPath(path)
	viper.AddConfigPath(".")
	viper.SetConfigName(".env")
	viper.SetConfigType("env")
	viper.AutomaticEnv()

	err := viper.ReadInConfig()
	if err != nil {
		return nil, err
	}

	err = viper.Unmarshal(&config)
	if err != nil {
		return nil, err
	}
	return &config, nil
}
