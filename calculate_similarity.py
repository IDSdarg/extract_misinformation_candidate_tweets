import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

sbert = SentenceTransformer('bert-base-nli-mean-tokens')

dat = pd.read_csv('./res/replies.csv')

sbert_embs = np.array(sbert.encode(dat.tweet, show_progress_bar=True, batch_size=10))

official_advice = "No, antibiotics do not work against viruses, only bacteria. The new coronavirus (2019-nCoV) is a virus and, therefore, antibiotics should not be used as a means of prevention or treatment. However, if you are hospitalized for the 2019-nCoV, you may receive antibiotics because bacterial co-infection is possible."

advice_embs = sbert.encode([official_advice], show_progress_bar=False)
sims = cosine_similarity(advice_embs, sbert_embs)
sims = sims.flatten()

dat = dat.assign(sim=sims)
dat = dat.sort_values(by=['sim'], ascending=False)

dat.to_csv("./res/replies_with_sims.csv", index=False)
print("Saved in ./res/replies_with_sims.csv")
