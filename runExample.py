import sys
import MathExample #In this example, one checkpoint is made at the time of importing.



def main():
    import time
    time.sleep(2) #adding a delay so that there will be a separate timestamp and thus separate checkpoint compared to the import MathExample statement.    
    list = [4, 23, 55, 34, 76, 92, 45, 52, 2, 16]
    #print("Computing properties of these numbers : " + str(list))
    #print("Mean : ", MathExample.mean(list))
    #print("Variance : ", MathExample.sample_variance(list))
    print("Computing Std Dev of these numbers : " + str(list))
    print("Std Dev : ", MathExample.std_dev(list)) 
    
    #In this example, the "Immediate Export" to the checkpoints log is turned off for the individual function calls, so we call export citation checkpoints at the end.
    MathExample.export_citation_checkpoints()
 
    #However, that still does not create a citesoft consolidated software log.
    #We will do so below -- though this could of course be done by a wrapper within the dev-user's module.
    import CiteSoft
    CiteSoft.compile_consolidated_log()
if __name__ == '__main__':
    main()
