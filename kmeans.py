import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from kneed import KneeLocator
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

# Creation d'un jeu de données artificielles
features, labels_vrai = make_blobs(n_samples=200, centers=3, cluster_std=1.75, random_state=42)
df=pd.DataFrame(features)
print(df.head(n=3))

# renommage de colonne
df.columns=['f1','f2']
df.rename(columns = {'f1':'x','f2':'y'},inplace=True)
# ajout d'une colonne
df["labels"]=labels_vrai

print(df.head(n=3))

sns.pairplot(df)


sse = []
Kmax=50
for k in range(1, Kmax):
    kmeans = KMeans(init="random",n_clusters=k,n_init=10,max_iter=300,random_state=42)
    kmeans.fit(features)
    sse.append(kmeans.inertia_)

plt.style.use("fivethirtyeight")
plt.plot(range(1, Kmax), sse)
plt.xticks(range(1, Kmax))
plt.xlabel("Nombres de groupes/Clusters")
plt.ylabel("inertie SSE")
plt.title("analyse de l'inertie intra classe")