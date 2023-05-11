import pickle

import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

df_all_values = pd.read_csv('./modeling.csv')
df_article_cluster = pd.read_csv('./articles_clusters.csv')
df_TRS_TR_OneCus = pd.read_csv('./Customer_Articles.csv')
similar_items_df = pd.read_csv('./similar_items.csv')

print("Loading Model")
# Load the model from the file
with open('lgbm_model.pkl', 'rb') as file:
    lgbm_model = pickle.load(file)

print(
    "Choosing a customer and its previous products and using them to predict")

customer_id = '0095c9b47fc950788bb709201f024c5338838a27c59c0299b857f94b504cb9fc'
articles = df_TRS_TR_OneCus[df_TRS_TR_OneCus['customer_id'] ==
                            customer_id]['articles'].values[0]

# Split the article_ids into a list of individual articles
article_list = articles.split(',')
article_list = [article[1:] for article in article_list]
# Convert the elements in article_list to integers
article_list = [int(article) for article in article_list]

print('This customer has bought product', article_list[-1])

# Filter the entries in df_all_values based on the article_id list
each_product_modeled_data = df_all_values[df_all_values['article_id'].isin(
    article_list)]
each_product_modeled_data = each_product_modeled_data.reset_index(drop=True)
each_product_modeled_data = each_product_modeled_data.drop('article_id',
                                                           axis=1).iloc[-1]

print("Predicting")
prediction = lgbm_model.predict(each_product_modeled_data.to_numpy().reshape(
    1, -1))

predictions = df_article_cluster[df_article_cluster.cluster ==
                           prediction[0]][:7]['article_id'].values

print(predictions)

PATH = './data/images/'


# def showPrediction(predictionsDF,
#                    transactionsDF,
#                    rows=2,
#                    columns=7,
#                    figsize=(20, 10)):
#
#     predictions = list(predictionsDF)
#     bought_items = transactionsDF[transactionsDF["customer_id"] == customer_id].iloc[0]['articles'].split(",")
#
#     print(bought_items)
#     print(predictions)
#
#     f, ax = plt.subplots(rows, columns, figsize=figsize)
#     for i in range(rows):
#         index = 0
#         for j in range(columns):
#             if i == 0:
#                 try:
#                     img_path = f'{PATH}{str(bought_items[index])[:3]}/0{int(bought_items[index])}.jpg'
#                     img = Image.open(img_path)
#                     ax[i, j].imshow(img)
#                     ax[i, j].set_xticks([], [])
#                     ax[i, j].set_yticks([], [])
#                     ax[i, j].grid(False)
#                     ax[i, j].set_title("Bought")
#                     index += 1
#                 except IndexError:
#                     continue
#             else:
#                 try:
#                     img_path = f'{PATH}0{str(predictions[index])[:2]}/0{int(predictions[index])}.jpg'
#                     img = Image.open(img_path)
#                     ax[i, j].imshow(img)
#                     ax[i, j].set_xticks([], [])
#                     ax[i, j].set_yticks([], [])
#                     ax[i, j].grid(False)
#                     ax[i, j].set_title("Prediction")
#                     index += 1
#                 except IndexError:
#                     continue
#     plt.tight_layout()
#     plt.show()


# showPrediction(predictions, df_TRS_TR_OneCus)

def show_similar_to_predictions(predictionsDF,
                                similar_items_df,
                                rows=10,
                                columns=8,
                                figsize=(20, 10)):
    predictions = list(predictionsDF)

    print(predictions)

    # Find similar items for each predicted item
    similar_items = []
    for item_id in predictions:
        similar_items.append(similar_items_df[similar_items_df["item"] == item_id]["similar_items"].iloc[0])

    similar_items = [list(map(int, s[1:-1].split(', '))) for s in similar_items]

    # Flatten the list of similar items and remove duplicates
    similar_items = list(
        set([item for sublist in similar_items for item in sublist]))

    print(similar_items)
    # Print the recommended items
    # print(f"Recommended items for customer {customer_id}: {similar_items}")

    # Show the images of the recommended items
    f, ax = plt.subplots(rows, columns, figsize=figsize)
    for i in range(rows):
        for j in range(columns):
            index = i * columns + j
            if index < len(similar_items):
                try:
                    img_path = f'{PATH}0{str(similar_items[index])[:2]}/0{int(similar_items[index])}.jpg'
                    img = Image.open(img_path)
                    ax[i, j].imshow(img)
                    ax[i, j].set_xticks([], [])
                    ax[i, j].set_yticks([], [])
                    ax[i, j].grid(False)
                    ax[i, j].set_title("Recommended")
                except IndexError:
                    continue
            else:
                break

    plt.tight_layout()
    plt.show()


show_similar_to_predictions(predictions, similar_items_df)
