// encode package include a set of functions to handle encoding and decoding.
package encode

import (
	"bytes"
	"encoding/json"
	"errors"
	"io"
	"log"
	"net/http"
	"todo-api-golang/pkg/apierror"

	"github.com/gorilla/mux"
)

// WriteResponse sets the status code and the response body using response writer.
func WriteResponse(rw http.ResponseWriter, code int, data any) {
	rw.Header().Add("Content-Type", "application/json")
	rw.WriteHeader(code)
	if err := json.NewEncoder(rw).Encode(data); err != nil {
		log.Printf("Write response failed: %v", err)
		rw.WriteHeader(http.StatusInternalServerError)
	}
}

// WriteError sets the status code and the response body of an ErrorResponse using response writer.
func WriteError(rw http.ResponseWriter, error *apierror.ErrorResponse) {
	rw.Header().Add("Content-Type", "application/problem+json")
	rw.WriteHeader(error.Code)

	if err := json.NewEncoder(rw).Encode(error); err != nil {
		log.Printf("Write error failed: %v", err)
	}
}

// GetUriParam returns the value of a http uri param.
func GetUriParam(r *http.Request, uriParam string) (string, error) {
	vars := mux.Vars(r)
	queryParam, ok := vars[uriParam]
	if !ok {
		return "", errors.New("invalid uri param")
	}
	return queryParam, nil
}

// ReadRequestBody decodes the json body of an http request.
func ReadRequestBody(r *http.Request, data any) error {
	return json.NewDecoder(r.Body).Decode(data)
}

// ReadResponseBody decodes the json body of an http response.
func ReadResponseBody(r *http.Response, data any) error {
	return json.NewDecoder(r.Body).Decode(data)
}

// CreateRequest encodes a struct to a io reader interface.
func CreateRequest(data any) (io.Reader, error) {
	var buf bytes.Buffer
	err := json.NewEncoder(&buf).Encode(data)
	if err != nil {
		return nil, err
	}
	return &buf, nil
}
