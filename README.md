# Semantic_search

A semantic search backend service

### Prerequisites

#### 1. Install with pip from source

```
pip install -r requirments.txt
```

### Services APIs, and Deployment & Testing

#### Services APIs

| API             | Description                                                  |
| --------------- | ------------------------------------------------------------ |
| **check_collection_exist** | POST request to check specific collection if exist|
| **get_qa_pairs** | POST request to get all qa pairs|
| **upload_qa_pairs** | POST request to upload qa pairs |
| **qa_search** | POST request to search Similar QA|

#### Deployment
##### Start command

```
python api_server.py --port <port_num> --config_path <config_path> 
eg: python api_server.py --port 3011 --config_path './conf/config_test_aramus_qa.ini'
```

## Repository Organization

### `/`

| Subfolder                                                    | Description                                                  |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [log] | Log will be stored in the /log/<application_name> folder |
| [uploaded] | All uploaded QA files will be saved in /uploaded/<application_name> folder |
| [conf] | All config files need to be set here |

### Acknowledgements

* Mingsheng was responsible for the all semantic search backend service.
* Jinyu was responsible for the frontend interface.
* Fenglin was responsible for the backend service include workflow, FAQ management system etc.

