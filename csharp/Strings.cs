using System;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;

namespace StackWizard
{
    /// <summary>
    /// String manipulation operations for performance benchmarking.
    /// Tests string reversal, concatenation, and pattern matching.
    /// </summary>
    public class Strings
    {
        /// <summary>
        /// Reverse a string.
        /// </summary>
        public static string ReverseString(string str)
        {
            char[] charArray = str.ToCharArray();
            Array.Reverse(charArray);
            return new string(charArray);
        }

        /// <summary>
        /// Concatenate a string n times.
        /// </summary>
        public static string ConcatenateString(string baseStr, int n)
        {
            var sb = new StringBuilder();
            for (int i = 0; i < n; i++)
            {
                sb.Append(baseStr);
            }
            return sb.ToString();
        }

        /// <summary>
        /// Find 5-letter words in text using pattern matching.
        /// </summary>
        public static int FindFiveLetterWords(string text)
        {
            var regex = new Regex(@"\b[a-zA-Z]{5}\b");
            var matches = regex.Matches(text);
            return matches.Count;
        }

        /// <summary>
        /// Run string manipulation benchmarks.
        /// </summary>
        public static void RunBenchmark()
        {
            Console.WriteLine("\n=== String Manipulation Benchmarks ===");

            // 1. String Reversal (1 million characters)
            string longString = new string('a', 500000) + new string('b', 500000);
            var watchReverse = Stopwatch.StartNew();
            string reversed = ReverseString(longString);
            watchReverse.Stop();
            double timeReverse = watchReverse.Elapsed.TotalMilliseconds;
            Console.WriteLine($"String Reversal (1M chars): {timeReverse:F2} ms");

            // 2. String Concatenation (10,000 iterations)
            var watchConcat = Stopwatch.StartNew();
            string concatenated = ConcatenateString("test", 10000);
            watchConcat.Stop();
            double timeConcat = watchConcat.Elapsed.TotalMilliseconds;
            Console.WriteLine($"String Concatenation (10K iterations): {timeConcat:F2} ms");

            // 3. Pattern Search (find 5-letter words)
            string sampleText = "hello world quick brown foxes jumps over fence under table chair grape mango apple berry water glass plate metal stone brick house happy smile dream peace light stars night";
            string largeText = string.Concat(Enumerable.Repeat(sampleText + " ", 1000));
            var watchSearch = Stopwatch.StartNew();
            int matchCount = FindFiveLetterWords(largeText);
            watchSearch.Stop();
            double timeSearch = watchSearch.Elapsed.TotalMilliseconds;
            Console.WriteLine($"Pattern Search: {timeSearch:F2} ms ({matchCount} matches)");
        }
    }
}
