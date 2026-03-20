"""
Streamlit demo for RAG.

This is basically adding a streamlit interface on top of the code
in 1_embeddings.py. 
"""

import pandas as pd
import streamlit as st
from sentence_transformers import SentenceTransformer
import cohere
from scipy.spatial.distance import cdist
import numpy as np


@st.cache_data
def load_data():
    """
    Load dataset and pre-compute embeddings once
    """
    df = pd.read_csv('Hotel_Reviews.csv')
    df = df.head(500)  # Leave this line for protoyping, comment for full dataset
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(df.Positive_Review, show_progress_bar=True)

    return df, embeddings, model


def search(model, cohere_client, df, embeddings, user_request):
    """
    Perform the search (see notebook for details).

    Parameters:
        model: SentenceTransformer
            The sentence transformer model to compute embeddings.
        cohere_client: cohere.Client
            The Cohere client to perform the chat calls.
        df: pd.DataFrame
            The dataframe containing the hotel reviews.
        embeddings: np.array
            The pre-computed embeddings of the reviews.
        user_request: str
            The natural language request by the user.
        
    Returns:
        second_prompt: str
            The formatted information retrieved from the dataset to be used in the second call.
        final_response: str
            The final response by the model after considering the retrieved information.

    """
    prompt = """
    The user is going to ask a question. You should respond normally.
    However, if the user asks for hotels with good reviews in a certain
    category, respond solely REQUEST_HOTEL and then a description of the provided request.
    For example, if the user asks for "hotels with good breakfast and service",
    you should respond solely "REQUEST_HOTEL: good breakfast and service".
    Don't miss any word from the request.
    The message by the user is:
    """

    response = cohere_client.chat(
        message=prompt + user_request,
    )

    st.text(response.text)

    parts = response.text.split(":")
    if parts[0] == "REQUEST_HOTEL":
        # Perform search
        query = parts[1]
        # Compute the embedding of the query
        query_vector = model.encode([query])
        # Compute all distances and get top 10
        distances = cdist(query_vector, embeddings, 'cosine')
        top10 = np.argsort(distances)[0][0:10]

        # Show the top 10 (just for control)
        second_prompt = "Here are some reviews of specific hotels:\n"
        formatted_message = "#### Retrieved documents\n\n"
        for idx in top10:
            # Add positive review and hotel name to response
            second_prompt += f"Hotel: {df.Hotel_Name.values[idx]}\n"
            second_prompt += f"Review: {df.Positive_Review.values[idx]}\n\n"

            formatted_message += f"Review {idx} (**{df.Hotel_Name.values[idx]}**)\n\n * \"{df.Positive_Review.values[idx]}\"\n\n"

        # Eventually do the second call with all the information:
        response2 = cohere_client.chat(
            message="Now respond to the original request of the user, but take into account the following information:\n" + second_prompt,
            chat_history=response.chat_history,
        )

        return formatted_message, response2.text


def main():
    """
    Run the streamlit app.
    """
    with open("../cohere.key", encoding="utf-8") as f:
        cohere_api_key = f.read()

    cohere_client = cohere.Client(cohere_api_key)

    with st.spinner("Loading data and computing embeddings"):
        df, embeddings, model = load_data()

    user_request = st.text_input('Search for hotels')

    if st.button('Search'):
        second_prompt, final_response = search(model, cohere_client, df,
                                               embeddings, user_request)

        col1, col2 = st.columns(2)
        with col1:
            st.write(second_prompt)

        with col2:
            st.write("#### Final recommendation")
            st.info(final_response)


if __name__ == '__main__':
    main()
