import csv
import pandas as pd
from nltk.tokenize import sent_tokenize as sent
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def process_handout(file):
	data = pd.read_excel(file)
	lng_outcomes = data['Learning Outcomes'].values
	topics = data['Topics to be covered'].values
	unit_mapping = data['Units'].values
	return lng_outcomes,topics,unit_mapping


def check_level(question):
	levels = []
	if any(word in question for word in remember):
		levels.append(1)
	if any(word in question for word in understand):
	 	# print "q is in second level"
	 	levels.append(2)
	if any(word in question for word in applying):
	 	# print "q is in third level"
		levels.append(3)
	if any(word in question for word in analyze):
	 	# print "q is in fourth level"
	 	levels.append(4)
	if any(word in question for word in evaluate):
	 	# print "q is in fifth level"
	 	levels.append(5)
	if any(word in question for word in create):
	 	# print "q is in sixth level"
	 	levels.append(6)
	if len(levels) == 0:
		return 0
	return levels

def classify_difficulty_levels(question_dict):
	no_easy, no_medium, no_diff = 0,0,0
	class_dict = {}
	for k,v in question_dict.iteritems():
		if any(i in [6] for i in v):
			class_dict[k] = 'hard'
		elif any(i in [4,5] for i in v):
			class_dict[k] = 'medium'
		elif any(i in [1,2,3] for i in v):
			class_dict[k] = 'easy'

	return class_dict

def topic_processing(topics_dict):
	topic_key_value_pairs = {}
	for t in topics_dict:
		topics_to_dict = t.split(':')
		all_topics = topics_to_dict[1].split(',')
		all_topics = [str(x) for x in all_topics]
		topic_key_value_pairs[topics_to_dict[0]] = all_topics
	return topic_key_value_pairs

def map_question_topic(question,topic_dictionary,no):
	topic_map_res = {}
	for k,v in topic_dictionary.iteritems():
		if any(word in question for word in v):
			topic_map_res[i] = k
			break
	return topic_map_res

remember = ('Choose','Define','Find','How','Label','List','Match','Name','Omit','Recall','Relate','Select','Show','Spell','Tell','What','When','Where','Which','Who','Why')
remember = [x.lower() for x in remember]
understand = ('Classify','Compare','Contrast','Demonstrate','Explain','Extend','Illustrate','Infer','Interpret','Outline','Relate','Rephrase','Show','Summarize','Translate')
understand = [x.lower() for x in understand]
applying = ('apply','build','choose','construct','develop','experiment','identify','interview','make use of','model','organize','plan','select','solve','utilize')
applying = [x.lower() for x in applying]
analyze = ('Analyze','Assume','Categorize','Classify','Compare','Conclusion','Contrast','Discover','Dissect','Distinguish','Divide','Examine','Function','Inference','Inspect','List','Motive','Relationships','Simplify','Survey','Take part in','Test for','Theme')
analyze = [x.lower() for x in analyze]
evaluate = ('Agree','Appraise','Assess','Award','Choose','Compare','Conclude','Criteria','Criticize','Decide','Deduct','Defend','Determine','Disprove','Estimate','Evaluate','Explain','Importance','Influence','Interpret','Judge','Justify','Mark','Measure','Opinion','Perceive','Prioritize','Prove','Rate','Recommend','Rule on','Select','Support','Value')
evaluate = [x.lower() for x in evaluate]
create = ('Adapt','Build','Change','Choose','Combine','Compile','Compose','Construct','Create','Delete','Design','Develop','Discuss','Elaborate','Estimate','Formulate','Happen','Imagine','Improve','Invent','Make up','Maximize','Minimize','Modify','Original','Originate','Plan','Predict','Propose','Solution','Solve','Suppose','Test','Theory')
create = [x.lower() for x in create]
topics = []
files = ['handout.xlsx','ir_qp_mkp.xlsx','IR_sample.xlsx']
q_dict = {}
topic_dictionary = {}
probable_topic_all = []
for k in range(3):
	if k==0:
		values,dummy,topics_dict = process_handout(files[k])
		topic_dictionary = topic_processing(topics_dict)
	else:
		data = pd.read_excel(files[k])
		values = data['Question'].values
	i = 1
	for v in values:
		v = v.lower()
		ans = check_level(v)
		q_dict[i] = ans
		if k!=0:
			probable_topic = map_question_topic(v,topic_dictionary,i)
			probable_topic_all.append(probable_topic)
		else:
			continue
		if ans != 0:
			ans_str = ', '.join(map(str,ans))
		else:
			ans_str = 'Could not be classified.'
		print("Question " + str(i)+" is in "+ ans_str)
		i+=1
	print 'Possible Classification of questions into easy, medium, hard'
	classify = classify_difficulty_levels(q_dict)
	levels = list(classify.values())
	e_cnt, m_cnt, h_cnt = 0,0,0
	if k!=0:
		for l in levels:
			if l == 'easy':
				e_cnt+=1
			elif l == 'medium':
				m_cnt+=1
			else:
				h_cnt+=1

		print 'No. of easy questions are: ' + str(e_cnt)
		print 'No. of medium questions are: ' + str(m_cnt)
		print 'No. of hard questions are: ' + str(h_cnt)
	print '*****************************************'
	if k!=0:
		print 'The questions topic-wise is as follows:\n'
		print 'Note: Few of the questions could not be mapped.\n'
		for top in probable_topic_all:
			for q,t in top.iteritems():
				print 'Question number '+ str(q) + ' is probably from the topic number '+ str(t) + '\n'
	print '*****************************************'