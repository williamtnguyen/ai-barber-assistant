### Agentic Playground

This package currently does not properly use brazil, you'll need to install and use `uv`

#### Toy Haircut Agentic Application
- `hair0`: A FastAPI Web Application server that spins up AWS Strands agent(s) and serves a React SPA UI for users to get value from the agents via chat interface. It intends to use self-hosted Mem0 memory layer for rich, personalized converational experience (TODO). For now there is a "monolithic agent" that handles all intended features:
  - Hairstyle Consultation: Can insightfully suggest suitable hairstyles for a client:
    - a face image they submit (agent to rely on `face_shape_resolver_service` to deduce face shape) (DONE)
    - the client's appointment frequency to infer their hairstyle maintenance preferences (agent to rely on `get_appointment_frequency` tool) (TODO)
  - Haircut Appointment Booking: Can take in natural language queries and book appointments for clients while providing transparency of barber's schedule (TODO)

Available tooling
- `face_shape_resolver_service`: An MCP based face shape descriptor service that uses Google MediaPipe face mesh/landmarks to derive face ratios of a submitted face image and categorize the client's face shape. The above agent connects to this service via MCP Streamable HTTP transport. (DONE)
- `search_knowledge_base`: A locally defined tool searches for relevant documents in a simulated knowledge base/vector DB based on keywords in a user query (DONE). This will eventually be an actual knowledge base/vector DB (TODO)