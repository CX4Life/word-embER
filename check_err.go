package main

import (
	"fmt"
	"os"	
)

// CheckErr takes an error, and prints it to console
func CheckErr(err error){
	if err != nil {
		fmt.Println("Encountered error:", err)
		os.Exit(1)
	}
}