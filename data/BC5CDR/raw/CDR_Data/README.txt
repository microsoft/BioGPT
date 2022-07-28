===========================================================================
*
*                            PUBLIC DOMAIN NOTICE
*               National Center for Biotechnology Information
*
*  This software/database is a "United States Government Work" under the
*  terms of the United States Copyright Act.  It was written as part of
*  the author's official duties as a United States Government employee and
*  thus cannot be copyrighted.  This software/database is freely available
*  to the public for use. The National Library of Medicine and the U.S.
*  Government have not placed any restriction on its use or reproduction.
*
*  Although all reasonable efforts have been taken to ensure the accuracy
*  and reliability of the software and data, the NLM and the U.S.
*  Government do not and cannot warrant the performance or results that
*  may be obtained by using this software or data. The NLM and the U.S.
*  Government disclaim all warranties, express or implied, including
*  warranties of performance, merchantability or fitness for any 
*  particular purpose.
*
*  Please cite the authors in any work or product based on this material:
*
*  1. Wei CH, Peng Y, Leaman R, Davis AP, Mattingly CJ, Li J, Wiegers TC, 
*     Lu Z. Overview of the BioCreative V Chemical Disease Relation (CDR) 
*     Task, Proceedings of the Fifth BioCreative Challenge Evaluation Workshop, 
*     p154-166, 2015 
*
*  2. Li J, Sun Y, Johnson RJ, Sciaky D, Wei CH, Leaman R, Davis AP, Mattingly CJ,
*     Wiegers TC, Lu Z. Anotating chemicals, diseases and their interactions in 
*     biomedical literature, Proceedings of the Fifth BioCreative Challenge 
*     Evaluation Workshop, p173-182, 2015 
*
*  3. Leaman R, Dogan RI, Lu Z. DNorm: disease name normalization with pairwise 
*     learning to rank, Bioinformatics 29(22):2909-17, 2013
* 
*  4. Leaman R, Wei CH, Lu Z. tmChem: a high performance approach for chemical 
*     named entity recognition and normalization. J Cheminform, 7:S3, 2015
*
*
==========================================================================

This directory contains the annotated corpus created and used in the BioCreative 
V Chemical Disease Relation (CDR) Challenge Task [1]. In addition, it contains 
text-mined results of two computational tools for disease & chemcial NER. All data
are made available in both BioC XML and PubTator text formats. 

./CDR.Corpus: The annotated CDR corpus of 1500 PubMed articles of chemicals, 
diseases, and chemical-induced disease relationships [2]. 

./DNorm.TestSet: The text-mined results of diseases on the test set using DNorm [3].
		 The normalization performance is 0.81 (P), 0.80 (R), and 0.81 (F). 

./tmChem.TestSet: The text-mined results of chemicals on the test set using tmChem [4].
		  The normalization performance is 0.92 (P), 0.90 (R), and 0.91 (F). 

