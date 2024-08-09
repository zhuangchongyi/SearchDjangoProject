# platform = sys.platform
# print("当前系统:", platform)
# jieba.load_userdict("templates/dict.dic")
# text = "女性接听 不是咨询公司也不是要开户，说没有咨询过任何项目"
# words = pseg.lcut(text)  # jieba默认模式
# print(words)
# jieba.enable_paddle()  # 启动paddle模式。 0.40版之后开始支持，早期版本不支持
# if 'win' not in platform:
#     jieba.enable_parallel(4)
#
# words = pseg.lcut(text, use_paddle=True)  # paddle模式
# print(words)
"""
标签	含义	标签	含义	标签	含义	标签	含义
n	普通名词	f	方位名词	s	处所名词	t	时间
nr	人名	ns	地名	nt	机构名	nw	作品名
nz	其他专名	v	普通动词	vd	动副词	vn	名动词
a	形容词	ad	副形词	an	名形词	d	副词
m	数量词	q	量词	r	代词	p	介词
c	连词	u	助词	xc	其他虚词	w	标点符号
PER	人名	LOC	地名	ORG	机构名	TIME	时间
"""
