import filters as f
import preprocess as p

def no_prep(text):
  return text


def no_usernames(text):
  return f.no_usernames(text)

def remove_noise(text):
  text = f.no_url(text)
  text = f.no_usernames(text)
  text = f.hash_as_normal(text)
  text = f.no_rt_tag(text)
  text = f.reduce_letter_duplicates(text)
  # text = p.negation_attachment(text)
  return text

def remove_all(text):
  text = f.no_url(text)
  text = f.no_usernames(text)
  text = f.no_hash(text)
  text = f.no_emoticons(text)
  text = f.no_rt_tag(text)
  return text

def placeholders(text):
  text = f.url_placeholder(text)
  text = f.username_placeholder(text)
  text = f.hash_placeholder(text)
  return text

def reduced_attached(text):
  text = f.reduce_letter_duplicates(text)
  text = p.negation_attachment(text)
  return text

def no_url_usernames_reduced_attached(text):
  text = f.no_url(text)
  text = f.no_usernames(text)
  text = f.reduce_letter_duplicates(text)
  text = p.negation_attachment(text)
  return text

def all(text):
  text = text.lower()
  text = f.no_url(text)
  text = f.no_usernames(text)
  text = f.no_emoticons(text)
  text = f.no_hash(text)
  text = f.no_rt_tag(text)
  text = f.reduce_letter_duplicates(text)
  text = p.negation_attachment(text)

  return text