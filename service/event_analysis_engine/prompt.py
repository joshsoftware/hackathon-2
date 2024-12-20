EVENT_ANALYSIS_PROMPT = """
Analyze the provided data containing analytical events and error logs to identify details about failed events and their related logs. Your task is to:
1. Look at the failed analytical events (both frontend and backend).
2. Cross-reference them with error logs (frontend and backend) to identify which logs are related to which failed event.
3. Provide insights into why each event failed (possible reasons behind the failure).
4. Determine if the failure is fixable or not.
5. Add any additional relevant remarks.

Output Format:
Return your findings as a JSON object with the following structure:

```json
{
    "result": [
        {
            "event_id": "", // uuid of this event
            "logs": [1, 2, 3], // IDs of the logs related to this event failure
            "reason": "", // one of these: ad-blocker-plugin,ad-blocking-browser,network-failure,browser-policy,service-unavailability
            "insights": ["insight 1", "insight 2"], // Insights about what went wrong
            "fixable": false, // True if the issue is fixable, false otherwise
            "remark": "" // Additional detailed remarks
        }
    ]
}
```

Important: The response must be in JSON format only, without any additional text or explanation.

Data:
Frontend Analytical Failed Events:
<FE_EVENTS>

Backend Analytical Failed Events:
<BE_EVENTS>

Error Logs:
<FE_LOGS>

Backend:
<BE_LOGS>

Analyze the data, identify the relationships, reasons, fixability, and remarks for the failed events, and respond strictly in the specified JSON format.
"""