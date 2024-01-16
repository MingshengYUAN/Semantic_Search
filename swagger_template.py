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
        "summary": "Upload Excel file that meets specifications",
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
              "$ref": "#/definitions/ApiResponse"
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
              "$ref": "#/definitions/ApiResponse"
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
              "$ref": "#/definitions/input_text"
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
    }
  }
}