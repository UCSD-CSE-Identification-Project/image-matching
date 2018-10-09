#import the necessary packages
from PIL import Image
import pytesseract
import cv2
import os
import numpy as np

# returns the number of changes required to make string 2 into string 1
def editDistDP( str1, str2):
  m = len(str1)
  n = len(str2)
  # Create a table to strore rsults of subproblems
  dp = [[0 for x in range(n+1)] for x in range(m+1)]

  # Fill d[][] in bottom up manner
  for i in range(m+1):
    for j in range(n+1):
      
      if i == 0:
        dp[i][j] = j

      elif j == 0:
        dp[i][j] = i

      elif str1[i - 1] == str2[j-1]:
        dp[i][j] = dp[i-1][j-1]

      else:
        dp[i][j] = 1 + min( dp[i][j-1], dp[i-1][j], dp[i-1][j-1])

  return dp[m][n]