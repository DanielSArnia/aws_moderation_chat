system_string = (
    "You are a creative nickname generator for a child platform.\n",
    "Your task is to create fun, appropriate, child-friendly nicknames that align with the child platform's brand values and comply with all safety regulations for children's platforms."
)

input_template = (
    "Generate 10 unique nicknames with the following parameters:\n",
    "\n",
    "User Age: {age_range}\n",
    "User Interests: {interests} (e.g., \"space, dinosaurs, pirates\")\n",
    "Themes They Like: {themes} (e.g., \"City, Star Wars\")\n",
    "Region: {region_code}\n",
    "\n",
    "Requirements:\n",
    "1. Each nickname must be child-appropriate and safe\n",
    "2. Length between 3-15 characters\n",
    "3. No personal information\n",
    "4. Align with the child platform's creative, positive brand\n",
    "5. Incorporate elements from their interests or favorite themes\n",
    "6. Be unique and memorable\n",
    "7. Include a brief explanation of each nickname's inspiration\n",
    "\n",
    "Return your response as JSON:\n",
    "{{\n",
    "  \"nicknames\": [\n",
    "    {{\n",
    "      \"nickname\": \"<nickname_1>\",\n",
    "      \"inspiration\": \"<brief explanation>\",\n",
    "      \"theme_connection\": \"<related theme>\"\n",
    "    }},\n",
    "    ...\n",
    "  ]\n",
    "}}"
)

system_string_batch_verification = (
    "You are evaluating a batch of generated nicknames for the child platform platform against safety and compliance guidelines."
)

input_template_batch_verification = (
    "Review the following batch of generated nicknames for a children's platform:\n",
    "\n",
    "Nicknames: {nicknames}\n",
    "User Age Range: {age_range}\n",
    "Region: {region_code}\n",
    "\n",
    "For each nickname, determine if it passes all validation checks:\n",
    "1. Free of inappropriate content\n",
    "2. Contains no personal information\n",
    "3. Aligns with a child platform's brand values\n",
    "4. Age-appropriate\n",
    "5. Complies with regional regulations\n",
    "\n",
    "Return your analysis as JSON with a \"pass\" boolean True/False:\n",
    "Make sure you generate a valid JSON with the following format for each nickname:",
    "{{\n",
    "  \"validation_results\": [\n",
    "    {{\n",
    "      \"nickname\": \"<nickname_1>\",\n",
    "      \"passes_validation\": <boolean>,\n",
    "      \"issues\": [\"<issue_1>\", \"<issue_2>\"] or [],\n",
    "      \"risk_level\": \"<none|low|medium|high>\"\n",
    "    }},\n",
    "    ...\n",
    "  ]\n",
    "}}"
)

tool_list_validate = [
    {
        "toolSpec": {
            "name": "validate_nicknames",
            "description": "Validate a list of nicknames, providing validation results, potential issues, and risk levels.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "validation_results": {
                            "type": "array",
                            "description": "A list containing validation results for each nickname.",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "nickname": {
                                        "type": "string",
                                        "description": "The nickname being validated.",
                                    },
                                    "passes_validation": {
                                        "type": "boolean",
                                        "description": "Indicates whether the nickname passed validation checks.",
                                    },
                                    "issues": {
                                        "type": "array",
                                        "description": "A list of issues found with the nickname, or an empty list if none.",
                                        "items": {"type": "string"},
                                    },
                                    "risk_level": {
                                        "type": "string",
                                        "description": "The assessed risk level of the nickname.",
                                        "enum": ["none", "low", "medium", "high"],
                                    },
                                },
                                "required": [
                                    "nickname",
                                    "passes_validation",
                                    "issues",
                                    "risk_level",
                                ],
                            },
                        }
                    },
                    "required": ["validation_results"],
                }
            },
        }
    }
]

tool_list_generate = [
    {
        "toolSpec": {
            "name": "generate_nicknames",
            "description": "Generate a list of nicknames based on themes.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "nicknames": {
                            "type": "array",
                            "description": "A list of nicknames generated based on themes.",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "nickname": {
                                        "type": "string",
                                        "description": "The generated nickname.",
                                    },
                                    "inspiration": {
                                        "type": "string",
                                        "description": "A brief explanation of the inspiration for the nickname.",
                                    },
                                    "theme_connection": {
                                        "type": "string",
                                        "description": "The theme related to the nickname.",
                                    },
                                },
                                "required": [
                                    "nickname",
                                    "inspiration",
                                    "theme_connection",
                                ],
                            },
                        }
                    },
                    "required": ["nicknames"],
                }
            },
        }
    }
]
