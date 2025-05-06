# Simple RAG
* Step 1) Extract text from a pdf
* Step 2) Split the Text into smaller chunks
* Step 3) Convert the chunks into numerical Embeding (DocEmbedding)
* Step 4) Input User Query
* Step 5) Embedding the User Query (QueryEmbedding)
* Step 6) Search for the most relevent chunks based on the Query Embedding (Search QueryEmbedding from DocEmbedding)
* Step 7) Compare the response with the correct answer to evaluate accuracy.
