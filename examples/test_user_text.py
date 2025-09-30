#!/usr/bin/env python3
"""
Test script using the exact text provided by the user
"""

from question_maker import TextTransformer, extract_multiple_choice_questions

# The exact text provided by the user
USER_PROVIDED_TEXT = """Which of the following is an essential amino acid in humans?
A Tyrosine
B Glutamine
C Glutamate
D Phenylalanine
E Lysine
The term "ketogenic" describes an amino acid that:
A is a precursor for glucose synthesis.
B forms oxaloacetate during catabolism.
C cannot be converted to ketone bodies.
D degrades to give a-ketoglutarate.
E is catabolised to yield acetyl CoA or acetoacetyl CoA.
Which of the following statements regarding glutamate dehydrogenase is INCORRECT?
A It can use either NAD+ or NADP+ as a coenzyme.
B It catalyses an essentially reversible reaction.
C When catalysing the conversion of glutamate to its carbon skeleton, the reaction involves deamination.
D It is not subject to allosteric regulation.
E It is located in the mitochondria.
How is glutamate useful in amino acid synthesis reactions?
A It activates glutaminase to release free glutamine.
B It can be reduced and cyclised to form glycine.
C It acts as an amino group donor for synthesis of nonessential amino acids.
D It is the main precursor of tyrosine synthesis.
E It is the main methyl group donor for essential amino acids.
Which of the following statements is correct?
A In humans, nonessential amino acids are exclusively synthesised from essential amino acids.
B Humans can attain nonessential amino acids from a protein-rich diet.
C Alanine is a common methyl group donor in human essential amino acid synthesis.
D In humans, aspartate is formed from pyruvate and is therefore a nonessential amino acid.
E All nonessential amino acids are catabolised to form acetoacetate.
Which of the following statements regarding tyrosine in humans is correct?
A Tyrosine is an essential amino acid as it cannot be synthesised.
B Catecholamines are formed following deamination of tyrosine.
C Tyrosine is the main precursor of carnitine in the liver.
D Tyrosine is commonly converted directly to serotonin or melatonin.
E Tyrosine is an important precursor of thyroxine in the thyroid gland.
Which of the following is an important role of ornithine in humans?
A It is one of the 20 common amino acids in all of our proteins.
B It is a key intermediate in the TCA cycle, combining with acetyl CoA to form citrate.
C It is an intermediate in the urea cycle in the kidney.
D It is one of two ways that NH3 groups can travel safely in blood.
E It is required for the cyclisation of proline.
Which of the following statements regarding the urea cycle in humans is INCORRECT?
A It aids in the excretion of nitrogen from the body.
B It is linked to the TCA cycle through fumarate.
C It occurs mainly in the liver and kidney.
D It is reduced when the activity of carbamoyl phosphate synthase I is activated.
E All reactions occur in the cytosol.
Which of the following best describes the energy needs of the urea cycle?
A 6 ATP equivalents: 4 as ATP → ADP and 2 as GTP → GDP.
B 4 ATP equivalents: 2 as ATP → ADP and 1 as ATP → AMP.
C 2 ATP equivalents: 2 as ATP → ADP, plus 2 NADH → NAD+.
D 3 ATP equivalents: 2 as ATP → ADP and 1 as ATP → AMP.
E The urea cycle does not require energy input as it is a catabolic cycle breaking down ammonia.
The primary function of the urea cycle is to:
A produce ATP.
B synthesise amino acids.
C detoxify ammonia.
D generate NADH.
E produce urine.
Which amino acid is involved in the transport of nitrogen from peripheral tissues to the liver?
A Methionine
B Glutamine
C Leucine
D Valine
E Isoleucine
What is a primary role of glutamate dehydrogenase in amino acid catabolism?
A Conversion of glutamate to alpha-ketoglutarate
B Synthesis of glutamine from glutamate
C Oxidation of amino acids for energy
D Formation of urea from ammonia
E Conversion of ammonia to urea
C cannot be converted to ketone bodies.
D degrades to give a-ketoglutarate.
E is catabolised to yield acetyl CoA or acetoacetyl CoA.
Which of the following statements regarding glutamate dehydrogenase is INCORRECT?
A It can use either NAD+ or NADP+ as a coenzyme.
B It catalyses an essentially reversible reaction.
C When catalysing the conversion of glutamate to its carbon skeleton, the reaction involves deamination.
D It is not subject to allosteric regulation.
E It is located in the mitochondria.
How is glutamate useful in amino acid synthesis reactions?
A It activates glutaminase to release free glutamine.
B It can be reduced and cyclised to form glycine.
C It acts as an amino group donor for synthesis of nonessential amino acids.
D It is the main precursor of tyrosine synthesis.
E It is the main methyl group donor for essential amino acids."""


def main():
    """Test with the user-provided text"""
    print("=== Testing with User-Provided Text ===\n")
    
    # Use TextTransformer
    transformer = TextTransformer()
    transformer.add_processor(extract_multiple_choice_questions)
    
    result = transformer.transform(USER_PROVIDED_TEXT, source_type='string')
    
    mc_data = result.extracted_data
    print(f"Total questions found: {mc_data['question_count']}")
    print(f"Questions with options: {mc_data['questions_with_options']}")
    print(f"Text length: {len(result.content)} characters")
    print()
    
    # List all questions with their first few words
    print("Questions extracted:")
    print("-" * 50)
    for i, question_data in enumerate(mc_data['multiple_choice_questions'], 1):
        question_text = question_data['question']
        # Truncate long questions for display
        if len(question_text) > 70:
            question_text = question_text[:67] + "..."
        print(f"{i:2d}. {question_text}")
        print(f"    Options: {', '.join(sorted(question_data['options'].keys()))}")
    
    print(f"\n{'-'*50}")
    
    # Show a few complete questions as examples
    print("\nExample questions (first 3):")
    for i, question_data in enumerate(mc_data['multiple_choice_questions'][:3], 1):
        print(f"\n--- Question {i} ---")
        print(question_data['question'])
        for label in sorted(question_data['options'].keys()):
            print(f"{label} {question_data['options'][label]}")


if __name__ == "__main__":
    main()