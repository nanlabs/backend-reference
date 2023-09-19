// note package include application logic related with the note sub feature.
package note

import "github.com/go-playground/validator"

// CustomValidator is a common interface for custom validators.
type CustomValidator interface {
	IsValid() bool
}

// ValidateEnum is a custom validator to validate if the input is within the list of valid values.
func ValidateEnum(fl validator.FieldLevel) bool {
	value := fl.Field().Interface().(CustomValidator)
	return value.IsValid()
}
