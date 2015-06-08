# LanguageID
This is a self-contained Language Identification system that is able to determine what human language a string of text has been written in. The Project uses the Flask module to expose the language identification functionality through a RESTful API.

This system comes pre-trained in four languages:
* `English, Spanish, French, German`

The training data has been collected from:
* `JRC-Acquis` (http://optima.jrc.it/Acquis/JRC-Acquis.3.0/corpus/)

# Model Training
For each language, a Markov Model is trained from a text corpus. In these models, each state represents character trigrams. The parameters of the model are the transition probabilities. Since, it is only possible to transition from c1c2c3 to c2c3c4, the transition probability reduces to nothing but the 4-gram probability, `P(c4|c1c2c3)`.

These probabilities are calculated using MLE. Hence, the probabilities are the relative frequencies for each transition in the training data.

# Language Detection
To detect the language of a new input text, the sequence probability is computed using each language model it has been trained for. Finally, the one with the largest probability is chosen to be the detected language.

# Adding New Languages
The JRC-Acquis corpus contains XML documents for a large number of languages.
* Update `NEW_LANGS` list in config.py with the new languages that are to be added.
* Update the `ROOTDIR` and `TARGETDIR` paths in config.py
* Download and uncompress the folder corresponding to the chosen language into the `ROOTDIR`.
* Run `python index.py`
* Run `python createModel.py`
* Update the `LANG` and `LANGUAGE_NAMES` lists in config.py with the new languages that have been added.

# Testing the system
* Start the REST service by executing the command `python app.py`.
* Open a new console window and type in the following command:

  `curl -i -H "Content-Type: application/json" -X POST -d '{"text":"test sentence"}' http://localhost:5000/lang_id`
* The 'text' field can be updated with the test sentence.
* The response is generated in JSON.
