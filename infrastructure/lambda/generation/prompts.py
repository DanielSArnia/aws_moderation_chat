system_string = (
    "You are a creative nickname generator for the LEGO platform.\n",
    "Your task is to create fun, appropriate, child-friendly nicknames that align with LEGO's brand values and comply with all safety regulations for children's platforms."
)

input_template = (
    "Generate 10 unique nicknames with the following parameters:\n",
    "\n",
    "User Age: {age_range}\n",
    "User Interests: {interests} (e.g., \"space, dinosaurs, pirates\")\n",
    "LEGO Themes They Like: {lego_themes} (e.g., \"LEGO City, LEGO Star Wars\")\n",
    "Region: {region_code}\n",
    "\n",
    "Requirements:\n",
    "1. Each nickname must be child-appropriate and safe\n",
    "2. Length between 3-15 characters\n",
    "3. No personal information\n",
    "4. Align with LEGO's creative, positive brand\n",
    "5. Incorporate elements from their interests or favorite LEGO themes\n",
    "6. Be unique and memorable\n",
    "7. Include a brief explanation of each nickname's inspiration\n",
    "\n",
    "Return your response as JSON:\n",
    "{{\n",
    "  \"nicknames\": [\n",
    "    {{\n",
    "      \"nickname\": \"<nickname_1>\",\n",
    "      \"inspiration\": \"<brief explanation>\",\n",
    "      \"theme_connection\": \"<related LEGO theme>\"\n",
    "    }},\n",
    "    ...\n",
    "  ]\n",
    "}}"
)

system_string_batch_verification = (
    "You are evaluating a batch of generated nicknames for the LEGO platform against safety and compliance guidelines."
)

input_template_batch_verification = (
    "Review the following batch of generated nicknames for a children's LEGO platform:\n",
    "\n",
    "Nicknames: {nicknames}\n",
    "User Age Range: {age_range}\n",
    "Region: {region_code}\n",
    "\n",
    "For each nickname, determine if it passes all validation checks:\n",
    "1. Free of inappropriate content\n",
    "2. Contains no personal information\n",
    "3. Aligns with LEGO's brand values\n",
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
