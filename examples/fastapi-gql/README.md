# FastApi GraphQl with relational database

## Prerequistes

- Python
  - Debian/Ubuntu

    ```bash
        apt install python3```

  - MacOS

    ```bash
        brew install python@3```

- Virtualenv

    ```bash
    pip3 install virtualenv```

## Install steps

1. Create and Activate virtual environment

    ```bash
    virtualenv -p python3 env
    source env/bin/activate
    ```

2. Install the requirements from requirements.txt

    ```bash
        pip install -r requirements.txt```

## Usage

- Start up application

    ```bash
        python src/main.py```

- Open GraphQl

    ```bash
        # Follow the URL for GraphQl playground
        http://0.0.0.0:8000/graphql
    ```

## Quering on GraphQl

- Queries

  - AllCompanies

    ```json
        query AllCompanies {
            __typename
            getCompanies {
                ... on CompaniesResponseList {
                    companies {
                        id
                        companyName
                        address
                        city
                        country
                        country
                        zipCode
                        timeZone
                        ownerName
                        ownerLastName
                        email
                        phoneNumber
                        taxId
                    }
                }
                ... on CompanyListError {
                    message
                }
            }
        }

    ```

  - Company (with Factory create)

    ```json
        query Company {
            company {
                ... on CompanyResponse {
                    id
                    companyName
                    address
                    city
                    country
                    country
                    zipCode
                    timeZone
                    ownerName
                    ownerLastName
                    email
                    phoneNumber
                    taxId
                }
                ... on GetCompanyError {
                    message
                }
            }
        }

    ```
