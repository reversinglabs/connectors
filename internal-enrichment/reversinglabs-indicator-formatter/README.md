# ReversingLabs Indicator Formatter

The ReversingLabs Indicator Formatter connector supports enrichment of observables by updating stix Indicator field “name” with the pattern.value

The connector works for the following observable types in OpenCTI:

- Stix-file
- Url 
- Domain-Name
- IPv4-Addr


## Installation

### Requirements

- OpenCTI Platform >= 6.5.8


### Example setup using Docker

1. Clone the repo from Github to your environment or OpenCTI instance
2. Position to /connectors/internal-enrichment/reversinglabs-indicator-formatter
3. Build the image using the Docker build command: docker build -t opencti/connector-reversinglabs-indicator-formatter . 
4. Run the image using Docker compose command: docker compose up -d
5. Ensure that the container is up and running: docker ps | grep indicator
6. Check that the connector is active, enabled and working in OpenCTI UI -> http://opencti_ip:8080/dashboard/data/ingestion/connectors
7. Monitor the progress of the formating jobs under: http://opencti_ip:8080/dashboard/data/ingestion/connectors/(RL_Indicator_Formatter_uuid) -> In progress works
8. Check the IOC's and Observables names under http://opencti_ip:8080/dashboard/observations/indicators

### Configuration

Configuration parameters are provided using environment variables as described below. Some of them are placed directly in the `docker-compose.yml` since they are not expected to be modified by final users once that they have been defined by the developer of the connector.

Expected environment variables to be set in the  `docker-compose.yml` that describe the connector itself. Most of the time, these values are NOT expected to be changed.

| Parameter                            | Docker envvar                       | Mandatory    | Description                                                                                                                                                |
| ------------------------------------ | ----------------------------------- | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `connector_name`                     | `CONNECTOR_NAME`                    | Yes          | A connector name to be shown in OpenCTI.                                                                                                                   |
| `connector_scope`                    | `CONNECTOR_SCOPE`                   | Yes          | Supported scope. E. g., `text/html`.                                                                                                                       |

However, there are other values which are expected to be configured by end users. The following values are expected to be defined in the `.env` file or `/etc/environments`. This file is included in the `.gitignore` to avoid leaking sensitive data).  Note that the `.env.sample` file can be used as a reference.

The ones that follow are connector's generic execution parameters expected to be added for export connectors.

| Parameter                            | Docker envvar                       | Mandatory    | Description                                                                                                                                                |
| ------------------------------------ | ----------------------------------- | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `opencti_url`                        | `OPENCTI_URL`                       | Yes          | The URL of the OpenCTI platform. Note that final `/` should be avoided. Example value: `http://opencti:8080`                                               |
| `opencti_token`                      | `OPENCTI_TOKEN`                     | Yes          | The default admin token configured in the OpenCTI platform parameters file.                                                                                |
| `connector_id`                       | `CONNECTOR_ID`                      | Yes          | A valid arbitrary `UUIDv4` that must be unique for this connector.                                                                                         |
| `connector_confidence_level`         | `CONNECTOR_CONFIDENCE_LEVEL`        | Yes          | The default confidence level for created sightings (a number between 1 and 4).                                                                             |
| `connector_log_level`                | `CONNECTOR_LOG_LEVEL`               | Yes          | The log level for this connector, could be `debug`, `info`, `warn` or `error` (less verbose).                                                              |
| `connector_auto`		       | `CONNECTOR_AUTO`		     | Yes	    | Enable or disable auto-enrichmnet on observable (default: false)												 |

### Debugging ###

The connector can be debugged by setting the appropiate log level.
Note that logging messages can be added using `self.helper.log_{LOG_LEVEL}("Sample message")`, i. e., `self.helper.log_error("An error message")`.


### Additional information
