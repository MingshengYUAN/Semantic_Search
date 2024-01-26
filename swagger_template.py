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
            "name": "token_name",
            "in": "formData",
            "description": "Token name",
            "required": True,
            "type": "string"
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
            "name": "token_name",
            "in": "formData",
            "description": "Specific token name for the excel or the task",
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
    "/empty_collection": {
      "post": {
        "tags": [
          "empty_collection"
        ],
        "summary": "Empty selected collections or all collections",
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
            "description": "Given token name or leave empty will empty all collections",
            "required": True,
            "schema": {
              "$ref": "#/definitions/collection_name"
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
    "collection_name": {
      "type": "object",
      "required": [
        "collection_name"
      ],
      "properties": {
        "collection_name": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "example": ["token_name"]
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
        "en_qa_list": {
          "items": {
            "type": "array"
          },
          "example": ["(en_Question, en_Answer)"]
        },
        "ar_qa_list": {
          "items": {
            "type": "array"
          },
          "example": ["(ar_Question, ar_Answer)"]
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