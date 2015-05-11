


package regression1;
import java.util.ArrayList;

import com.aliasi.tokenizer.NGramTokenizerFactory;
import com.aliasi.tokenizer.Tokenizer;
import com.aliasi.tokenizer.TokenizerFactory;
import com.aliasi.util.Strings;


/*@Uses: This will include some library like preprocessing etc
 * */
public class utill 
{
	
	
	static final TokenizerFactory NGRAM_TOKENIZER_FACTORY = new NGramTokenizerFactory(3,4);
	

	/*NGramTokenizerFactory  tokFact
	=  new  NGramTokenizerFactory(minNGramInt,maxNGramInt);*/
	public String pre_process(String source)
	{
		
		return source;
		
	}

	public String[] getngram(String source)
	{
	
		char cs[] = Strings.toCharArray(source);
		Tokenizer tk  = NGRAM_TOKENIZER_FACTORY.tokenizer(cs, 0, cs.length);
		 
		String tok_arr[] = tk.tokenize();
		int i= 0 ;
		return tok_arr;
		
	}
	
	public double compute_similiarity (String[] val1, String[] val2)
	{
		
		double score= 0.0;
		String[] sor  =  val1;  //saving to restore later tokenizers are exhausted in travarsal
		String[] tar =  val2;
		
		ArrayList<count_freq>  source_freq =  new ArrayList<count_freq>(); 
		ArrayList<count_freq>  target_freq =  new ArrayList<count_freq>(); 
		
		
		for(String tok1: val1)
		{
			for(String tok2: val2)
			{
				
				if(tok1.toString().equalsIgnoreCase(tok2.toString()))
				{
				
		           score = score  + tok1.toString().length();			
				}
				
			}
		}
		
		val1  =  sor;
		val2 =  tar;
		
		source_freq = compute_word_and_freq (source_freq, val1);
		target_freq = compute_word_and_freq (target_freq, val2);
		
		double len1 = compute_length (source_freq);
		double len2  = compute_length(target_freq);
		double len_multi =  len1 * len2;
		
		if(score!=0)
		{
		 
		  score =  score/len_multi;
		  score =  score *1000;
		}	
			
	return score;	
	}
	
	
	private double compute_length(ArrayList<count_freq> source_freq) 
	{
		double len = 0.0;
		for(int i=0;i<source_freq.size();i++)
		{
			len =  len + source_freq.get(i).count * source_freq.get(i).count;
		}
		
		
		len = Math.sqrt(len);
		return len;
	}

	private ArrayList<count_freq> compute_word_and_freq( ArrayList<count_freq> source_freq, String[] val1) 
	{
		
		//source frequency calculation
				for(String tok1: val1 )
				{
					boolean flag =  false;
					int i;
					for(i=0;i<source_freq.size();i++ )
					{
						
						if(source_freq.get(i).str.equalsIgnoreCase(tok1))
						{
							flag =  true;
							break;
						}
					}
					
					if(flag ==false)
					 {
						count_freq obj =  new  count_freq(tok1, 1);
						source_freq.add(obj);
					 }//if
					else
					{
						int ngram_count =  source_freq.get(i).count;
						ngram_count++;
						count_freq obj =  new  count_freq(tok1, ngram_count);
						source_freq.set(i, obj);
					}//eslse
				}//for
				
		return source_freq;
	}

	public static void main(String args[])
	{
		utill u = new utill();
		String[] val1 = u.getngram("anggg");
		String[] val2 = u .getngram("ang1ang");
		
		/*for(String token: val1 )
		 {System.out.println("val = "+token);}	
		for(String token: val2 )
		 {System.out.println("val2 = "+token);}	*/
		
		double sim = u.compute_similiarity(val1, val2);
		
		System.out.println("sim="+sim);
		
	}//main
}
