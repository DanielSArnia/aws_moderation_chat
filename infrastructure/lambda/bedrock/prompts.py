system_string = (
    "You are evaluating a child's nickname for a child platform.\n",
    "Your task is to analyze this nickname against corporate guidelines, safety policies, and regulations.\n"
    "Provide a structured JSON response with detailed scores and explanations."
)

input_template = (
    "Evaluate the following nickname:\n",
    "\n",
    "Nickname: \"{nickname}\"\n",
    "Platform: Kids Community\n",
    "User Age Range: {age_range}\n",
    "Region: {region_code}\n",
    "\n",
    "Provide a detailed analysis covering:\n",
    "1. Inappropriate Content: Detect profanity, adult themes, violence, bullying, drugs, or other inappropriate content (even in coded language or slang)\n",
    "2. Personal Information: Identify potential PII including names, locations, ages, schools, or anything that could identify a child\n",
    "3. Brand Alignment: Assess if the nickname aligns with a child platform's positive, creative, family-friendly brand values\n",
    "4. Age Appropriateness: Determine if the nickname is suitable for all users in a children's platform\n",
    "5. Regional Compliance: Check for region-specific concerns relating to COPPA, GDPR, or other relevant regulations\n",
    "\n",
    "Return your analysis in the following JSON format:\n",
    "{{\n",
    "  \"analysis\": {{\n",
    "    \"inappropriate_content\": {{\n",
    "      \"score\": <0-1 value, lower is better>,\n",
    "      \"pass\": <boolean>,\n",
    "      \"explanation\": <string>\n",
    "    }},\n",
    "    \"personal_information\": {{\n",
    "      \"score\": <0-1 value, lower is better>,\n",
    "      \"pass\": <boolean>,\n",
    "      \"explanation\": <string>\n",
    "    }},\n",
    "    \"brand_alignment\": {{\n",
    "      \"score\": <0-1 value, higher is better>,\n",
    "      \"pass\": <boolean>,\n",
    "      \"explanation\": <string>\n",
    "    }},\n",
    "    \"age_appropriate\": {{\n",
    "      \"score\": <0-1 value, higher is better>,\n",
    "      \"pass\": <boolean>,\n",
    "      \"explanation\": <string>\n",
    "    }},\n",
    "    \"regional_compliance\": {{\n",
    "      \"pass\": <boolean>,\n",
    "      \"explanation\": <string>\n",
    "    }}\n",
    "  }},\n",
    "  \"overall_result\": {{\n",
    "    \"valid\": <boolean>,\n",
    "    \"confidence\": <0-1 value>,\n",
    "    \"decision_explanation\": <string>,\n",
    "    \"risk_level\": <\"none\"|\"low\"|\"medium\"|\"high\">\n",
    "  }}\n",
    "}}\n"
)

tool_list = [
    {
        "toolSpec": {
            "name": "analyze_nickname",
            "description": "Analyze nickname for inappropriate material, personal information, brand alignment, age appropriateness, and regional compliance. Returns an overall validation result and risk level.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "analysis": {
                            "type": "object",
                            "description": "Detailed analysis results for various compliance checks.",
                            "properties": {
                                "inappropriate_content": {
                                    "type": "object",
                                    "description": "Evaluation of inappropriate content.",
                                    "properties": {
                                        "score": {
                                            "type": "number",
                                            "description": "Score between 0 and 1; lower is better.",
                                            "minimum": 0,
                                            "maximum": 1,
                                        },
                                        "pass": {
                                            "type": "boolean",
                                            "description": "Whether the nickname passed the inappropriate content check.",
                                        },
                                        "explanation": {
                                            "type": "string",
                                            "description": "Explanation for the inappropriate content decision.",
                                        },
                                    },
                                    "required": ["score", "pass", "explanation"],
                                },
                                "personal_information": {
                                    "type": "object",
                                    "description": "Evaluation of personal information presence.",
                                    "properties": {
                                        "score": {
                                            "type": "number",
                                            "description": "Score between 0 and 1; lower is better.",
                                            "minimum": 0,
                                            "maximum": 1,
                                        },
                                        "pass": {
                                            "type": "boolean",
                                            "description": "Whether the nickname passed the personal information check.",
                                        },
                                        "explanation": {
                                            "type": "string",
                                            "description": "Explanation for the personal information decision.",
                                        },
                                    },
                                    "required": ["score", "pass", "explanation"],
                                },
                                "brand_alignment": {
                                    "type": "object",
                                    "description": "Evaluation of brand alignment.",
                                    "properties": {
                                        "score": {
                                            "type": "number",
                                            "description": "Score between 0 and 1; higher is better.",
                                            "minimum": 0,
                                            "maximum": 1,
                                        },
                                        "pass": {
                                            "type": "boolean",
                                            "description": "Whether the nickname aligns with the brand.",
                                        },
                                        "explanation": {
                                            "type": "string",
                                            "description": "Explanation for the brand alignment decision.",
                                        },
                                    },
                                    "required": ["score", "pass", "explanation"],
                                },
                                "age_appropriate": {
                                    "type": "object",
                                    "description": "Evaluation of age appropriateness.",
                                    "properties": {
                                        "score": {
                                            "type": "number",
                                            "description": "Score between 0 and 1; higher is better.",
                                            "minimum": 0,
                                            "maximum": 1,
                                        },
                                        "pass": {
                                            "type": "boolean",
                                            "description": "Whether the nickname is appropriate for the target age group.",
                                        },
                                        "explanation": {
                                            "type": "string",
                                            "description": "Explanation for the age appropriateness decision.",
                                        },
                                    },
                                    "required": ["score", "pass", "explanation"],
                                },
                                "regional_compliance": {
                                    "type": "object",
                                    "description": "Evaluation of regional compliance.",
                                    "properties": {
                                        "pass": {
                                            "type": "boolean",
                                            "description": "Whether the nickname complies with regional regulations.",
                                        },
                                        "explanation": {
                                            "type": "string",
                                            "description": "Explanation for the regional compliance decision.",
                                        },
                                    },
                                    "required": ["pass", "explanation"],
                                },
                            },
                            "required": [
                                "inappropriate_content",
                                "personal_information",
                                "brand_alignment",
                                "age_appropriate",
                                "regional_compliance",
                            ],
                        },
                        "overall_result": {
                            "type": "object",
                            "description": "Summary of the overall validation and risk assessment.",
                            "properties": {
                                "valid": {
                                    "type": "boolean",
                                    "description": "Indicates if the nickname passed all checks.",
                                },
                                "confidence": {
                                    "type": "number",
                                    "description": "Confidence score between 0 and 1.",
                                    "minimum": 0,
                                    "maximum": 1,
                                },
                                "decision_explanation": {
                                    "type": "string",
                                    "description": "Explanation for the overall validation decision.",
                                },
                                "risk_level": {
                                    "type": "string",
                                    "description": "Overall risk level associated with the nickname.",
                                    "enum": ["none", "low", "medium", "high"],
                                },
                            },
                            "required": [
                                "valid",
                                "confidence",
                                "decision_explanation",
                                "risk_level",
                            ],
                        },
                    },
                    "required": ["analysis", "overall_result"],
                }
            },
        }
    }
]
