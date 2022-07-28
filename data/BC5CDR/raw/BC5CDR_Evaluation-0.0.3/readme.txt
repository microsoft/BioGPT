[Directory]
A. Introduction
B. Installation
C. Instruction
D. Output control
E. Troubleshooting

#======================================================================================#

A. [Introduction]

	This is a set of scripts for executing a Java program for evaluating the performance of BioCreative V CDR task. Please follow the instructions to evaluate your system. We used DNorm, tmChem and coocurrence relations to develop a baseline results in the data/test folder.
	
	The three scripts each support both the PubTator (http://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/PubTator/) and BioC (http://bioc.sourceforge.net/) formats.

B. [Installation]

	Users need to install Java in their environment. Scripts are provided for the UNIX command line. Batch files for the Windows environment should be straightforward but are not provided.
	
C. [Instruction]

	This program can evaluate the performance of disease mention recognition (mention), normalization (id) and chemical-induces-disease relation (relation) on both PubTator and BioC formats.

	Instruction:

		./eval_mention.sh [BioC|PubTator] [gold standard] [result] 
		./eval_id.sh [BioC|PubTator] [gold standard] [result] 
		./eval_relation.sh [BioC|PubTator] [gold standard] [result] 

	Example mention evaluation:
		./eval_mention.sh PubTator data/gold/CDR_sample.gold.PubTator data/test/CDR_sample.test.DNER.PubTator
		OR
		./eval_mention.sh BioC data/gold/CDR_sample.gold.BioC.xml data/test/CDR_sample.test.DNER.BioC.xml

	Results:
		TP: 303
		FP: 105
		FN: 121
		Precision: 0.7426470588235294
		Recall: 0.714622641509434
		F-score: 0.7283653846153848
		
	Example ID evaluation:
		./eval_id.sh PubTator data/gold/CDR_sample.gold.PubTator data/test/CDR_sample.test.DNER.PubTator
		OR
		./eval_id.sh BioC data/gold/CDR_sample.gold.BioC.xml data/test/CDR_sample.test.DNER.BioC.xml
	
	Results:
		TP: 150
		FP: 56
		FN: 64
		Precision: 0.7281553398058253
		Recall: 0.7009345794392523
		F-score: 0.7142857142857142

	Example relation evaluation:
		./eval_relation.sh PubTator data/gold/CDR_sample.gold.PubTator data/test/CDR_sample.test.CID.PubTator
		OR
		./eval_relation.sh BioC data/gold/CDR_sample.gold.BioC.xml data/test/CDR_sample.test.CID.BioC.xml
	
	Results:
		TP: 90
		FP: 533
		FN: 33
		Precision: 0.14446227929373998
		Recall: 0.7317073170731707
		F-score: 0.24128686327077747

D. [Output control]

	The evaluation code provides some output useful for debugging but this is filtered by the scripts for simplicity. The information removed consists of a tab-delimited string containing the values necessary for determining if the the predicted values match the target values. This information is specific to each evaluation type.

	Mention evaluation:
		INFO	{TP|FP|FN}	mention	documentId	startOffset	endOffset	mentionType
	For example:
		INFO	TP	mention	1720453	34	48	Disease

	ID evaluation:
		INFO	{TP|FP|FN}	id	documentId	mentionType	conceptId
	For example:
		INFO	TP	id	7352670	Disease	MESH:D007022

	Relation evaluation
		INFO	{TP|FP|FN}	relation	documentId	relationType	conceptId1	conceptId2
	For example:
		INFO	TP	relation	2894766	CID	MESH:D012460	MESH:D011014

	To obtain the debug output for a specific evaluation, open the appropriate script, and change the Java command that is commented out (with the "#" symbol) to be the line that does not contain "grep -v INFO".
		
E. [Troubleshooting]

	The scripts are written to ignore some unexpected data. Writing data in the incorrect format may therefore result in it being ignored. Results with zero TP and zero FP are therefore probably indicating a formatting error.
	