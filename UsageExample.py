import sys
import MathExample



def main():
    list = [4, 23, 55, 34, 76, 92, 45, 52, 2, 16]
    print("Computing properties of these numbers : " + str(list))
    print("Mean : ", MathExample.mean(list))
    print("Variance : ", MathExample.sample_variance(list))
    print("Std Dev : ", MathExample.std_dev(list))
    #MathExample.export_citation("/home/christopher/Documents/")
    MathExample.export_citation()

if __name__ == '__main__':
    main()
