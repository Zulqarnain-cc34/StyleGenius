import pickle
import tkinter as tk
from tkinter import filedialog

import pandas as pd
# from PIL import Image
from PIL import Image, ImageTk

df_all_values = pd.read_csv('./modeling.csv')
df_article_cluster = pd.read_csv('./articles_clusters.csv')
df_TRS_TR_OneCus = pd.read_csv('./Customer_Articles.csv')
similar_items_df = pd.read_csv('./similar_items.csv')

print("Loading Model")
# Load the model from the file
with open('lgbm_model.pkl', 'rb') as file:
    lgbm_model = pickle.load(file)

df_all_values = df_all_values.reset_index(drop=True)

PATH = './data/images/'

# def showPrediction(predictionsDF,
#                    choosen_product,
#                    rows=2,
#                    columns=7,
#                    figsize=(20, 10)):
#
#     predictions = list(predictionsDF)
#     bought_items = list(choosen_product['article_id'])
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
#                     img_path = f'{PATH}0{str(bought_items[index])[:2]}/0{int(bought_items[index])}.jpg'
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


# def show_similar_to_predictions(predictionsDF,
#                                 similar_items_df,
#                                 rows=10,
#                                 columns=8,
#                                 figsize=(20, 10)):
#     predictions = list(predictionsDF)
#     print(predictions)
#
#     # Find similar items for each predicted item
#     similar_items = []
#     for item_id in predictions:
#         similar_items.append(similar_items_df[
#             similar_items_df["item"] == item_id]["similar_items"].iloc[0])
#
#     similar_items = [
#         list(map(int, s[1:-1].split(', '))) for s in similar_items
#     ]
#
#     # Flatten the list of similar items and remove duplicates
#     similar_items = list(
#         set([item for sublist in similar_items for item in sublist]))
#
#
#     # print(f"Recommended items for customer {customer_id}: {similar_items}")
#
#     # Show the images of the recommended items
#     f, ax = plt.subplots(rows, columns, figsize=figsize)
#     for i in range(rows):
#         for j in range(columns):
#             index = i * columns + j
#             if index < len(similar_items):
#                 try:
#                     img_path = f'{PATH}0{str(similar_items[index])[:2]}/0{int(similar_items[index])}.jpg'
#                     img = Image.open(img_path)
#                     ax[i, j].imshow(img)
#                     ax[i, j].set_xticks([], [])
#                     ax[i, j].set_yticks([], [])
#                     ax[i, j].grid(False)
#                     ax[i, j].set_title("Recommended")
#                 except IndexError:
#                     continue
#             else:
#                 break
#
#     plt.tight_layout()
#     plt.show()


# show_similar_to_predictions(predictions, similar_items_df)


# def adjust_id(x):
#     '''Adjusts article ID code.'''
#     x = str(x)
#     if len(x) == 9:
#         x = "0" + x
#
#     return x


def find_article_by_image():
    def process_image():
        # Clear the output widget
        output.delete(1.0, tk.END)

        # Get the uploaded file
        file_path = filedialog.askopenfilename(
            filetypes=[('JPEG Image', '*.jpg'), ('JPEG Image', '*.jpeg')])
        if file_path:
            with open(file_path, 'rb'):
                # uploaded_content = file.read()
                # uploaded_image = Image.open(io.BytesIO(uploaded_content))

                # Get the filename without the extension
                filename = file_path.split('/')[-1].split('.')[0][1:]
                filename = f'0{filename}'

                product = df_all_values[df_all_values['article_id'] == int(filename)]

                product = product.drop('article_id', axis=1)
                print("Predicting")
                prediction = lgbm_model.predict(product.to_numpy().reshape(1, -1))
                predictions = df_article_cluster[df_article_cluster.cluster ==
                                 prediction[0]][:7]['article_id'].values

                predictions = list(predictions)

                # Find the article in the articles dataframe
                # article = articles.loc[int(filename)]
                # articles["article_id"] = articles["article_id"].apply(
                #     lambda x: adjust_id(x))
                # article = articles[articles['article_id'] == filename]

                # Display the article information
                if len(predictions) > 0:
                    # Find similar items for each predicted item
                    similar_items = []
                    for file in predictions:
                        print(f'0{file}')
                        similar_items.append(
                            similar_items_df[similar_items_df["item"] == int(f'0{file}')]["similar_items"].iloc[0])

                    # similar_items = similar_items[0]
                    # Convert the string to a list using eval()
                    new_similar_items = []
                    for product in similar_items:
                        new_similar_items.append(eval(product))

                    similar_items = new_similar_items
                    similar_items = list(set([item for sublist in similar_items for item in sublist]))

                    print(similar_items)

                    # Show the images of the recommended items
                    rows, columns = 10, 8
                    f = tk.Frame(root)
                    f.pack()
                    for i in range(rows):
                        for j in range(columns):
                            index = i * columns + j
                            if index < len(similar_items):
                                try:
                                    img_path = f'{PATH}0{str(similar_items[index])[:2]}/0{int(similar_items[index])}.jpg'
                                    img = Image.open(img_path)
                                    img = img.resize(
                                        (100, 100)
                                    )  # Adjust the size of the image as needed
                                    photo = ImageTk.PhotoImage(img)
                                    label = tk.Label(f, image=photo)
                                    label.image = photo
                                    label.grid(row=i, column=j)
                                    label.bind('<Button-1>',
                                               lambda event, index=index:
                                               show_recommended(event, index))
                                except IndexError:
                                    continue
                            else:
                                break
                    if len(similar_items) > 0:
                        button = tk.Button(root,
                                           text="Show Recommended",
                                           command=show_all_recommended)
                        button.pack()
                    else:
                        label = tk.Label(root, text="No similar items found.")
                        label.pack()
                else:
                    label = tk.Label(root, text="No matching article found.")
                    label.pack()

    def show_recommended(event, index):
        # Display the clicked image in a new window or perform any other action
        print(f"Clicked image index: {index}")

    def show_all_recommended():
        # Display all recommended images or perform any other action
        print("Showing all recommended images")

    # Create the main tkinter window
    root = tk.Tk()
    root.title("Find Article by Image")

    # Create the button to start processing
    button = tk.Button(root, text="Process Image", command=process_image)
    button.pack()

    # Create the output widget
    output = tk.Text(root, height=20, width=50)
    output.pack()

    # Start the tkinter event loop
    root.mainloop()


find_article_by_image()
