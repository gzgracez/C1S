# Capital 1 Summit Hackathon - Personal Finance Manager
January 2017
## Members:
* Grace, Kevin, David, Ryuji, Jaymo

## Feature implementation
https://docs.google.com/document/d/19srp9269Dl6eKLvKOAVfFVOMmxT6mQGQ19KW5ihy8xs/edit

## Background
At the Capital 1 Software Engineering Summit hackathon, our team created a service to help college students better manage their budget. Our service allows students to check their balance in different accounts, allocate funds towards future activies like buying textbooks, and get a suggested spending amount for common categories like groceries and gas using past transactions while accounting for committed allocations.

![alt text](https://github.com/gzgracez/PersonalBudgetAdvisor/assets/Cap1Architecture.png "Architecture")

## Implemtation

The three front-facing applications called the same set of functions to access the Nessie API and an Amazon mySQL RDS. Students are able to interact with our service using Amazon's Alexa, a flask web app, and a raspberry pi. 

Alexa was able to answer questions such as "how much do I have in my checking account" and "how much should I spend on groceries today", as well as accomodating for requests such as "allocate $10 for food on Friday".

A raspberry pi server also was in constant contact with the Nessie API and updated an LCD display with checking, savings, and credit a balances.

Finally, a flask web app hosted on AWS elastic beanstalk allows authenticated students to get a more detailed view of their account balances, spending history, allocations, and suggested spending.
