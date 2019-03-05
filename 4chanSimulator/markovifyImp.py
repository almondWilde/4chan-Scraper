import markovify
import nltk
#nltk.download('averaged_perceptron_tagger')
import re

class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = [ "::".join(tag) for tag in nltk.pos_tag(words) ]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence

# Get raw text as string.
with open("out.dat") as f:
    texta = f.read()
    texta.replace('>', '')
with open("LIBRARYOFCONGRESS.txt") as f:
    textb = f.read()

# # Build the model.
# text_model = markovify.Text(text, state_size=3)

# # Print five randomly-generated sentences
# print 'sentences:'
# for i in range(5):
#     print(text_model.make_sentence())

# print '\n\n\nshort sentences:'
# # Print three randomly-generated sentences of no more than 140 characters
# for i in range(3):
#     print(text_model.make_short_sentence(140))

#combining naive models
# model_a = markovify.Text(texta)
# model_b = markovify.Text(textb)

pmodela = POSifiedText(texta)
pmodelb = POSifiedText(textb)

pmodel_combo = markovify.combine( [ pmodela, pmodelb], [.3,1])


for i in range(5):
    print(pmodel_combo.make_sentence())

print '\n\n\nshort sentences:'
# Print three randomly-generated sentences of no more than 140 characters
for i in range(3):
    print(pmodel_combo.make_short_sentence(140))

# Naive model
# model_combo = markovify.combine([ model_a, model_b ], [ .3, 1 ])

# for i in range(5):
#     print(i,model_combo.make_sentence())

# print '\n\n\nshort sentences:'
# # Print three randomly-generated sentences of no more than 140 characters
# for i in range(3):
#     print(model_combo.make_short_sentence(140))

