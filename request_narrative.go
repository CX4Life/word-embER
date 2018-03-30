package main

import (
	"fmt"
	"io/ioutil"
	"encoding/json"
)

const credendtialsFN = "creds.json"

// Creds stores information concerning API credentials
type Creds struct{
	GrantType string
	ClientID string
	ClientSecret string
	Username string
	Password string
} 

func parseCredentialsFile(filename string) Creds{	
	bytez, err := ioutil.ReadFile(filename)
	CheckErr(err)
	
	var cred Creds
	json.Unmarshal(bytez, &cred)
	return cred
}


// GetNarratives takes an int AID and returns every narrative for the selected account
func main() {
	fmt.Println("Here we go")
	myCreds := parseCredentialsFile(credendtialsFN)
	fmt.Println(myCreds)
}
