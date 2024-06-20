template = {
  "swagger": "2.0",
  "info": {
    "title": "Semantic Search API",
    "description": "New semantic search",
    "version": "0.0.1"
  },
  "tags": [
    {
      "name": "Upload_qa_pairs",
      "description": "upload qa pairs excel"
    }
  ],
  "paths": {
    "/upload_qa_pairs": {
      "post": {
        "tags": [
          "upload_qa_pairs"
        ],
        "summary": "Upload Excel file that meets specifications form",
        "description": "",
        "consumes": [
          "multipart/form-data"
        ],
        "produces": [
          "application/json"
        ],
        "parameters": [
          {
            "name": "file",
            "in": "formData",
            "description": "excel to upload",
            "required": True,
            "type": "file"
          },
          {
            "name": "token_name",
            "in": "formData",
            "description": "Specific token name for the excel or the task",
            "required": True,
            "type": "string"
          },
          {
            "name": "application_name",
            "in": "formData",
            "description": "Specific application name",
            "required": True,
            "type": "string"
          }
        ],
        "responses": {
          "200": {
            "description": "Successful operation",
            "schema": {
              "$ref": "#/definitions/standard_res"
            }
          }
        }
      }
    },
    "/upload_google_qa_pairs": {
      "post": {
        "tags": [
          "upload_google_qa_pairs"
        ],
        "summary": "Upload Excel file from Google docs",
        "description": "",
        "consumes": [
          "multipart/form-data"
        ],
        "produces": [
          "application/json"
        ],
        "parameters": [
          {
            "name": "file_id",
            "in": "formData",
            "description": "google doc file id eg:<1SadGNSpLDt4ZuRD6N4xwCAPmJvlfTrm3>",
            "required": True,
            "type": "string"
          },
          {
            "name": "token_name",
            "in": "formData",
            "description": "Specific token name for the excel or the task",
            "required": True,
            "type": "string"
          },
          {
            "name": "application_name",
            "in": "formData",
            "description": "Specific application name",
            "required": True,
            "type": "string"
          }
        ],
        "responses": {
          "200": {
            "description": "Successful operation",
            "schema": {
              "$ref": "#/definitions/standard_res"
            }
          }
        }
      }
    },
    "/get_qa_pairs": {
      "post": {
        "tags": [
          "get_qa_pairs"
        ],
        "summary": "Get uploaded QA pairs",
        "description": "",
        "consumes": [
          "multipart/form-data"
        ],
        "produces": [
          "application/json"
        ],
        "parameters": [
          {
            "name": "application_name",
            "in": "formData",
            "description": "Application_name",
            "required": True,
            "type": "string"
          },
          {
            "name": "lang",
            "in": "formData",
            "description": "QA_pairs language",
            "required": True,
            "type": "string"
          },
          {
            "name": "start_index",
            "in": "formData",
            "description": "The start index of the QA pair",
            "required": True,
            "type": "integer"
          },
          {
            "name": "end_index",
            "in": "formData",
            "description": "The end index of the QA pair",
            "required": True,
            "type": "integer"
          }
        ],
        "responses": {
          "200": {
            "description": "Successful operation",
            "schema": {
              "$ref": "#/definitions/read_qa_pairs"
            }
          }
        }
      }
    },
    "/qa_search": {
      "post": {
        "tags": [
          "qa_search"
        ],
        "summary": "Find the most similar QA pairs",
        "description": "",
        "consumes": [
          "multipart/form-data"
        ],
        "produces": [
          "application/json"
        ],
        "parameters": [
          {
            "name": "question",
            "in": "formData",
            "description": "User questions",
            "required": True,
            "type": "string"
          },
          {
            "name": "application_name",
            "in": "formData",
            "description": "Specific application name",
            "required": True,
            "type": "string"
          }
        ],
        "responses": {
          "200": {
            "description": "Successful operation",
            "schema": {
              "$ref": "#/definitions/qa_response"
            }
          }
        }
      }
    },
    "/empty_application": {
      "post": {
        "tags": [
          "empty_application"
        ],
        "summary": "Empty selected application or all applications",
        "description": "",
        "consumes": [
          "application/json"
        ],
        "produces": [
          "application/json"
        ],
        "parameters": [
          {
            "in": "body",
            "name": "body",
            "description": "Given application name or leave empty will empty all application",
            "required": True,
            "schema": {
              "$ref": "#/definitions/application_name"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful operation",
            "schema": {
              "$ref": "#/definitions/standard_res"
            }
          }
        }
      }
    },
    "/del_files": {
      "post": {
        "tags": [
          "del_files"
        ],
        "summary": "Del selected token name(file)",
        "description": "",
        "consumes": [
          "application/json"
        ],
        "produces": [
          "application/json"
        ],
        "parameters": [
          {
            "in": "body",
            "name": "body",
            "description": "Given token names(file)",
            "required": True,
            "schema": {
              "$ref": "#/definitions/file_name"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful operation",
            "schema": {
              "$ref": "#/definitions/standard_res"
            }
          }
        }
      }
    }
  },
  "definitions": {
    "ApiResponse": {
      "type": "object",
      "properties": {
        "response": {
          "items": {
            "type": "string"
          },
          "example": "Save success!"
        },
        "status": {
          "items": {
            "type": "string"
          },
          "example": "Success!"
        },
        "running_time": {
          "items": {
            "type": "number"
          },
          "example": "0.0325"
        }
      }
    },
    "application_name": {
      "type": "object",
      "required": [
        "application_name"
      ],
      "properties": {
        "application_name": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "example": ["application_name"]
        }
      }
    },
    "file_name": {
      "type": "object",
      "required": [
        "application_name",
        "token_names"
      ],
      "properties": {
        "application_name": {
          "items": {
            "type": "string"
          },
          "example": "application_name"
        },
        "token_names": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "example": ["token_names"]
        }
      }
    },
    "standard_res": {
      "type": "object",
      "properties": {
        "response": {
          "items": {
            "type": "string"
          },
          "example": "XXX success!"
        },
        "status": {
          "items": {
            "type": "string"
          },
          "example": "Success!"
        },
        "running_time": {
          "items": {
            "type": "number"
          },
          "example": "0.0325"
        }
      }
    },
    "qa_response": {
      "type": "object",
      "properties": {
        "response": {
          "items": {
            "type": "string"
          },
          "example": "XXX success!"
        },
        "reference": {
          "items": {
            "type": "string"
          },
          "example": "From xxxx"
        },
        "status": {
          "items": {
            "type": "string"
          },
          "example": "Success!"
        },
        "running_time": {
          "items": {
            "type": "number"
          },
          "example": "0.0325"
        }
      }
    },
    "read_qa_pairs": {
      "type": "object",
      "properties": {
        "result_list": {
          "items": {
            "type": "array"
          },
          "example": ["(Question, Answer)"]
        },
        "list_len": {
          "items": {
            "type": "integer"
          },
          "example": 98
        },
        "status": {
          "items": {
            "type": "string"
          },
          "example": "Success!"
        },
        "running_time": {
          "items": {
            "type": "number"
          },
          "example": "0.0325"
        }
      }
    }
  }
}