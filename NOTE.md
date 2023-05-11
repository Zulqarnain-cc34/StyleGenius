Product Recommendation:
-----------------------

Here in this demo i have done away with the preprocessing pipeline and am using the data ready for model input. In actual production enviorment you will have to prepare 
the pipeline as well.

The modeling.csv has 4903 products prepared in prediction input form. So when you say i want to predict the recommendation for a product. Although I am allowing you to select an image using tkinter what is happening is that the filename of the image is also the article_id in the modeling.csv. So the preprocessed data for the image to be put as input has been put in modeling.csv.So only images that you select that have data in modeling will work which are 4903 out of 115000 something.

So the product is selected from the modeling.csv. I pass this prodcut to the model lgbm which i have imported. This model predicts the cluster in which the dataset lies in. Lets say for a product model predicts 16th cluster.

Note so the main thing that is helping are 2 things to make the model prediction:

1. The trained model lgbm which has been trained on 5000 products to cluster them.
2. Second is the dataset of predictions, after the model is trained on 5000 products.

The training make the model more accurate to give the correct cluster. Second the already predicted products that lie in different clusters are similar products
. For each cluster there are 200-300 items which we can use to recommend since we have 200-300 similar products in each cluster.

I see the cluster my product lies in a choose the top 7 products.

I combined another appraoch as well. It is i prepared a similarity search dataset. So for each product i have 10 similar products which i prepared using faiss similarity search. Each of the 115000 products have 10 recommendation in this one. So Now i have 70 predicted products.


4. Contains the data ready for input phase

        df_all_values = pd.read_csv('./modeling.csv')

5. Containes the 5000 already predicted entries the format is article_id, cluster, buying_count

        df_article_cluster = pd.read_csv('./articles_clusters.csv')

6.  Dataset made using 10000 transactions that have customer and the products they bought

        df_TRS_TR_OneCus = pd.read_csv('./Customer_Articles.csv')

7. Dataset prepared that matched similar items

        similar_items_df = pd.read_csv('./similar_items.csv')


I am using tkinter to upload Image.

Customer Recommendation:
-----------------------

Here in this demo i have done away with the preprocessing pipeline and am using the data ready for model input. In actual production enviorment you will have to prepare 
the pipeline as well.

The modeling.csv has 4903 products prepared in prediction input form. So when you say i want to predict the recommendation for a product. 

The customer has to be one from the df_TRS_TR_OneCus dataset. The product data for the articles bought by this customer is taken from the modeling.csv. So the article that the person has bought its preprocessed data is selected from the modeling.csv file. For each customer even though some have 2,3 4 or even more we only look at the latest product purchased. I pass this prodcut to the model lgbm which i have imported. This model predicts the cluster in which the dataset lies in. 

Lets say for a product model predicts 16th cluster. I have a dataset prepared by predicting the clusters for 5000 items. In each cluster there are 200-300 items. I see the cluster my product lies in a choose the top 7 products. Then i also have prepared a similarity search dataset. So for each product i have 10 similar products which i prepared using faiss similarity search. Each of the 115000 products have 10 recommendation in this one. So Now I have 70 predicted products.

1. Contains the data ready for input phase

        df_all_values = pd.read_csv('./modeling.csv')

2. Containes the 5000 already predicted entries the format is article_id, cluster, buying_count

        df_article_cluster = pd.read_csv('./articles_clusters.csv')

3.  Dataset made using 10000 transactions that have customer and the products they bought

        df_TRS_TR_OneCus = pd.read_csv('./Customer_Articles.csv')

4. Dataset prepared that matched similar items

        similar_items_df = pd.read_csv('./similar_items.csv')
