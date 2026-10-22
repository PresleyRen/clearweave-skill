# Published-paper and Chinese examples / 真实文本修改对照

[简体中文](scholarly-examples.zh-CN.md) · [Documentation index](README.md)

These are edited demonstrations of the cited public texts, not replacement publications. Original authors and source licenses are listed with each case. Revisions were produced by the current conversational assistant using ClearWeave 0.3.0 and reviewed by that same assistant. Source facts were not independently verified.

[Evaluation and provenance](evaluation-scholarly.md) · [Raw inputs](../evals/scholarly-2026-10-20/samples.json) · [Outputs](../evals/scholarly-2026-10-20/outputs.json)

## D19-1410 · Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks

Authors/source: Nils Reimers, Iryna Gurevych. [D19-1410](https://aclanthology.org/D19-1410/). License: CC-BY-4.0. Action: `edit`.

### Original / 原文

BERT (Devlin et al., 2018) and RoBERTa (Liu et al., 2019) has set a new state-of-the-art performance on sentence-pair regression tasks like semantic textual similarity (STS). However, it requires that both sentences are fed into the network, which causes a massive computational overhead: Finding the most similar pair in a collection of 10,000 sentences requires about 50 million inference computations (~65 hours) with BERT. The construction of BERT makes it unsuitable for semantic similarity search as well as for unsupervised tasks like clustering. In this publication, we present Sentence-BERT (SBERT), a modification of the pretrained BERT network that use siamese and triplet network structures to derive semantically meaningful sentence embeddings that can be compared using cosine-similarity. This reduces the effort for finding the most similar pair from 65 hours with BERT / RoBERTa to about 5 seconds with SBERT, while maintaining the accuracy from BERT. We evaluate SBERT and SRoBERTa on common STS tasks and transfer learning tasks, where it outperforms other state-of-the-art sentence embeddings methods.

### Revision / 修改稿

BERT (Devlin et al., 2018) and RoBERTa (Liu et al., 2019) have set a new state of the art on sentence-pair regression tasks such as semantic textual similarity (STS). However, both sentences must be fed into the network, creating substantial computational overhead: finding the most similar pair in a collection of 10,000 sentences requires about 50 million inference computations (~65 hours) with BERT. This architecture makes BERT unsuitable for semantic similarity search and unsupervised tasks such as clustering. We present Sentence-BERT (SBERT), a modification of the pretrained BERT network that uses siamese and triplet network structures to derive semantically meaningful sentence embeddings that can be compared using cosine-similarity. This reduces the time required to find the most similar pair from 65 hours with BERT / RoBERTa to about 5 seconds with SBERT, while maintaining BERT's accuracy. We evaluate SBERT and SRoBERTa on common STS and transfer learning tasks, where it outperforms other state-of-the-art sentence embedding methods.

### Edit record / 修改记录

- Corrected coordinated-subject have and relative-clause uses; changed sentence embeddings methods to sentence embedding methods.
- Retained citations, 10,000, 50 million, ~65 hours, 65 hours, about 5 seconds, comparison and accuracy claim.
- Removed publication-level framing and clarified the input requirement.
- Residual ambiguity: the final it could be read as SBERT or the evaluated pair. Retained rather than silently broaden the comparative claim; author/full-paper context needed.

## W19-5034 · ScispaCy: Fast and Robust Models for Biomedical Natural Language Processing

Authors/source: Mark Neumann, Daniel King, Iz Beltagy, Waleed Ammar. [W19-5034](https://aclanthology.org/W19-5034/). License: CC-BY-4.0. Action: `keep`.

### Original / 原文

Despite recent advances in natural language processing, many statistical models for processing text perform extremely poorly under domain shift. Processing biomedical and clinical text is a critically important application area of natural language processing, for which there are few robust, practical, publicly available models. This paper describes scispaCy, a new Python library and models for practical biomedical/scientific text processing, which heavily leverages the spaCy library. We detail the performance of two packages of models released in scispaCy and demonstrate their robustness on several tasks and datasets. Models and code are available at https://allenai.github.io/scispacy/.

### Revision / 修改稿

Despite recent advances in natural language processing, many statistical models for processing text perform extremely poorly under domain shift. Processing biomedical and clinical text is a critically important application area of natural language processing, for which there are few robust, practical, publicly available models. This paper describes scispaCy, a new Python library and models for practical biomedical/scientific text processing, which heavily leverages the spaCy library. We detail the performance of two packages of models released in scispaCy and demonstrate their robustness on several tasks and datasets. Models and code are available at https://allenai.github.io/scispacy/.

### Edit record / 修改记录

- Kept the source unchanged as a control. Despite introduces a real contrast; robust is an on-topic model property.
- Importance/performance adjectives state the authors’ assessment; a style-only edit did not invent measurements to replace them.

## D16-1264 · SQuAD: 100,000+ Questions for Machine Comprehension of Text

Authors/source: Pranav Rajpurkar, Jian Zhang, Konstantin Lopyrev, Percy Liang. [Original PDF, page 1](https://aclanthology.org/D16-1264.pdf). License: CC-BY-4.0. Action: `keep`.

### Original and retained output

We present the Stanford Question Answering Dataset (SQuAD), a new reading comprehension dataset consisting of 100,000+ questions posed by crowdworkers on a set of Wikipedia articles, where the answer to each question is a segment of text from the corresponding reading passage. We analyze the dataset to understand the types of reasoning required to answer the questions, leaning heavily on dependency and constituency trees. We build a strong logistic regression model, which achieves an F1 score of 51.0%, a significant improvement over a simple baseline (20%). However, human performance (86.8%) is much higher, indicating that the dataset presents a good challenge problem for future research. The dataset is freely available at https://stanford-qa.com.

The abstract is retained unchanged in this minimal-edit control. The transition to human performance expresses a substantive comparison. The XML omission was recovered from the attributed PDF excerpt and checked visually; the stored record keeps both provenance steps.

## W19-5028 · Clinical Concept Extraction for Document-Level Coding

Authors/source: Sarah Wiegreffe, Edward Choi, Sherry Yan, Jimeng Sun, Jacob Eisenstein. [W19-5028](https://aclanthology.org/W19-5028/). License: CC-BY-4.0. Action: `edit`.

### Original / 原文

The text of clinical notes can be a valuable source of patient information and clinical assessments. Historically, the primary approach for exploiting clinical notes has been information extraction: linking spans of text to concepts in a detailed domain ontology. However, recent work has demonstrated the potential of supervised machine learning to extract document-level codes directly from the raw text of clinical notes. We propose to bridge the gap between the two approaches with two novel syntheses: (1) treating extracted concepts as features, which are used to supplement or replace the text of the note; (2) treating extracted concepts as labels, which are used to learn a better representation of the text. Unfortunately, the resulting concepts do not yield performance gains on the document-level clinical coding task. We explore possible explanations and future research directions.

### Revision / 修改稿

The text of clinical notes can be a valuable source of patient information and clinical assessments. Historically, the primary approach for exploiting clinical notes has been information extraction: linking spans of text to concepts in a detailed domain ontology. However, recent work has demonstrated the potential of supervised machine learning to extract document-level codes directly from the raw text of clinical notes. We propose to bridge the gap between the two approaches with two novel syntheses: (1) treating extracted concepts as features, which are used to supplement or replace the text of the note; (2) treating extracted concepts as labels, which are used to learn a better representation of the text. The resulting concepts do not yield performance gains on the document-level clinical coding task. We explore possible explanations and future research directions.

### Edit record / 修改记录

- Removed the attitude marker Unfortunately, and left the negative finding unchanged.
- Retained the two distinct syntheses, the contrast with prior work, and the exploratory explanations. This is computational NLP research text, not clinical advice.

## W19-4703 · Studying Semantic Chain Shifts with Word2Vec: FOOD>MEAT>FLESH

Authors/source: Richard Zimmermann. [W19-4703](https://aclanthology.org/W19-4703/). License: CC-BY-4.0. Action: `edit`.

### Original / 原文

Word2Vec models are used to study the semantic chain shift FOOD>MEAT>FLESH in the history of English, c. 1425-1925. The development stretches out over a long time, starting before 1500, and may possibly be continuing to this day. The semantic changes likely proceeded as a push chain.

### Revision / 修改稿

Word2Vec models are used to study the semantic chain shift FOOD>MEAT>FLESH in the history of English, c. 1425-1925. This development began before 1500 and may be continuing to this day. The semantic changes likely proceeded as a push chain.

### Edit record / 修改记录

- Reduced a stacked possibility expression to may; retained likely, before 1500, and c. 1425-1925.
- To this day is part of the historical 2019 text; it was not updated to the current year.

## W19-4731 · Understanding the Evolution of Circular Economy through Language Change

Authors/source: Sampriti Mahanty, Frank Boons, Julia Handl, Riza Theresa Batista-Navarro. [W19-4731](https://aclanthology.org/W19-4731/). License: CC-BY-4.0. Action: `edit`.

### Original / 原文

In this study, we propose to focus on understanding the evolution of a specific scientific concept—that of Circular Economy (CE)—by analysing how the language used in academic discussions has changed semantically. It is worth noting that the meaning and central theme of this concept has remained the same; however, we hypothesise that it has undergone semantic change by way of additional layers being added to the concept. We have shown that semantic change in language is a reflection of shifts in scientific ideas, which in turn help explain the evolution of a concept. Focusing on the CE concept, our analysis demonstrated that the change over time in the language used in academic discussions of CE is indicative of the way in which the concept evolved and expanded.

### Revision / 修改稿

In this study, we propose to examine how Circular Economy (CE) has evolved by analysing semantic changes in the language of academic discussions. The meaning and central theme of CE have remained the same; however, we hypothesise that it has undergone semantic change through the addition of layers to the concept. We have shown that semantic change in language reflects shifts in scientific ideas, which in turn help explain a concept's evolution. Our analysis of CE demonstrated that changes over time in the language of academic discussions indicate how the concept evolved and expanded.

### Edit record / 修改记录

- Removed empty framing, corrected compound-subject have, and shortened nominalized wording.
- Kept propose, hypothesise, have shown and demonstrated as different source speech acts; retained the proposed semantic-layer explanation.
- The coexistence of stable meaning and semantic change is an author argument, not independently fact-checked here.

## HC3-ZH-CHATGPT-02188 · 如何评价莫言在诺贝尔文学奖颁奖仪式上的演讲在国内社交网络引起的反响？文字链接：

Authors/source: HC3 corpus / ChatGPT answer. [HC3-ZH-CHATGPT-02188](https://huggingface.co/datasets/Hello-SimpleAI/HC3-Chinese/resolve/09a687b8dc164b89e7df95abf15df3b216bc31c2/open_qa.jsonl). License: CC-BY-SA-4.0. Action: `edit`.

### Original / 原文

我无法给出关于莫言在诺贝尔文学奖颁奖仪式上的演讲在国内社交网络上的反响的评价，因为我是一个计算机程序，并不具备观看视频、阅读文字或使用社交媒体的能力。我无法了解国内的社交媒体上对莫言演讲的反响情况。我只能提供有关莫言的一般信息。

莫言（1955年2月17日出生）是中国著名的作家，2012年获得诺贝尔文学奖。他的作品涉及历史、文化、政治等多个领域，并被翻译成多种语言。莫言的作品深受读者喜爱，他在中国乃至世界范围内享有盛誉。

### Revision / 修改稿

我是计算机程序，无法观看视频、阅读文字或使用社交媒体，因此不了解莫言在诺贝尔文学奖颁奖仪式上的演讲在国内社交网络引起的反响，也无法作出评价。我只能提供莫言的一般信息。

莫言（1955年2月17日出生）是中国著名作家，2012年获得诺贝尔文学奖。他的作品涉及历史、文化、政治等领域，已被译成多种语言，深受读者喜爱，在中国及世界范围内享有盛誉。

### Edit record / 修改记录

- Compressed repeated inability statements while retaining the original speaker identity and capabilities claim.
- Retained full birth date, award year, thematic list, translations, reader popularity and reputation claim.
- Historical dataset answer, not a statement of the present assistant’s capabilities and not updated biographical verification.

## HC3-ZH-CHATGPT-02605 · 为什么人们那么喜欢看前男友前女友或者现男友现女友前任们的社交网络？（如微博）?

Authors/source: HC3 corpus / ChatGPT answer. [HC3-ZH-CHATGPT-02605](https://huggingface.co/datasets/Hello-SimpleAI/HC3-Chinese/resolve/09a687b8dc164b89e7df95abf15df3b216bc31c2/open_qa.jsonl). License: CC-BY-SA-4.0. Action: `edit`.

### Original / 原文

人们喜欢看到前男友前女友或者现男友现女友前任们的社交网络可能是出于好奇心或者比较关心对方的原因。有时候，人们会想知道对方在社交网络上发布了什么信息，或者对方的生活情况如何。此外，人们可能还有一些心理上的需求，比如想知道自己是否被前任取代了，或者是否还有机会和前任复合。

然而，在社交网络上看到前任的信息并不一定是一件好事。在某些情况下，这可能会让人感到不安或者心烦，特别是当前任对象在社交网络上发布了一些让人不满意的信息时。因此，最好的做法是保持一定的距离，不要把自己的情绪完全依赖于社交网络上的信息。

### Revision / 修改稿

人们喜欢查看前任，或现任伴侣的前任的社交网络，可能是出于好奇，也可能是比较关心对方。有时，人们想知道对方发布了什么，或近况如何，也可能有心理上的需求，比如想知道自己是否已被前任取代，或是否还有机会复合。

但看到前任的信息不一定是好事。在某些情况下，这可能让人不安或心烦，尤其是看到让自己不满意的内容时。因此，最好保持一定距离，不要让自己的情绪完全依赖社交网络上的信息。

### Edit record / 修改记录

- Shortened repeated relationship labels and transitions.
- Retained possibility, frequency, some circumstances, comparative concern, examples, negative assessment and recommendation.
- Self-review found no new personal experience or opinion; underlying psychological assertions were not verified.
- Targeted self-review restored 喜欢 and made the source disjunction explicit. Initial and final revisions are retained; this was not detected by literal comparison.

<details><summary>Initial draft before targeted self-review</summary>

人们查看前任，或现任伴侣的前任的社交网络，可能是出于好奇，也可能是比较关心对方。有时，人们想知道对方发布了什么、近况如何，也可能有心理上的需求，比如想知道自己是否已被前任取代，或是否还有机会复合。

但看到前任的信息不一定是好事。在某些情况下，这可能让人不安或心烦，尤其是看到让自己不满意的内容时。因此，最好保持一定距离，不要让自己的情绪完全依赖社交网络上的信息。

</details>
