tools = [
    {
        "type": "function",
        "function": {
            "name": "search_and_scrape_internships",
            "description": "Searches for internships on Internshala based on a profile, optional location, and how recently they were posted. Scrapes the results and saves them to a CSV file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "profile": {
                        "type": "string",
                        "description": "The job profile or keyword to search for, e.g., 'Web Development', 'Graphic Design'."
                    },
                    "location": {
                        "type": "string",
                        "description": "The city or location for the internship, e.g., 'Mumbai', 'Bangalore'."
                    },
                    "last_days": {
                        "type": "integer",
                        "description": "Filter internships posted within the last number of days. Common values are 1, 3, 7, 15, 30."
                    }
                },
                "required": ["profile"]
            }
        }
    }
]