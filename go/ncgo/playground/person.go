package playground

import (
	"errors"
	"fmt"
	"strings"
)

type TwitterHandle = string

type Identifiable interface {
	ID() string
}

type Person struct {
	firstName     string
	lastName      string
	twitterHandle TwitterHandle
}

func NewPerson(firstName, lastName string) Person {
	return Person{
		firstName: firstName,
		lastName:  lastName,
	}
}

func (p *Person) SetTwitterHandle(handle string) error {
	if len(handle) != 0 && !strings.HasPrefix(handle, "@") {
		return errors.New("Twitter handle must start with an @")
	}
	p.twitterHandle = handle
	return nil
}

func (p *Person) FullName() string {
	return fmt.Sprintf("%s %s", p.firstName, p.lastName)
}

func (p *Person) ID() string {
	return "ID500"
}
