#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org>
"""


def global_alignment(
    s_1,
    s_2,
    gap_score=-1,
    match_score=1,
    unmatch_score=-1,
    best_align_score=0
    ):
    """
    Needleman – Wunsch Algorithm.
    Global alignment algorithm using dynamic programming.

    Parameters
    ----------
    s_1 : str
        the first input sequence
    s_2 : str
        the second input sequence
    gap_score : int
    match_score : int
    unmatch_score : int
    best_align_score : int

    Returns
    s_out_1 : str
        the first output sequence
    s_out_2 : str
        the second output sequence
    -------
    """

    # length of sequences
    length_1 = len(s_1)
    length_2 = len(s_2)
    
    # initialize graph to calculate alignment score 
    graph = []
    for i in range(length_1 + 1):
        row = []
        for j in range(length_2 + 1):
            if i == 0:
                row.append(i * gap_score)
            else:
                if j == 0:
                    row.append(j * gap_score)
                else:
                    row.append(None)
        graph.append(row)

    # update the graph
    for i in range(length_1 + 1):
        for j in range(length_2 + 1):
            if i >= 1 and j >= 1:

                if s_1[i - 1] == s_2[j - 1]:
                    score_match = match_score
                else:
                    score_match = unmatch_score

                candidate_scores_list = []
                if graph[i - 1][j] is not None:
                    candidate_scores_list.append(graph[i - 1][j] + gap_score)
                if graph[i][j - 1] is not None:
                    candidate_scores_list.append(graph[i][j - 1] + gap_score)
                if graph[i - 1][j - 1] is not None:
                    candidate_scores_list.append(graph[i - 1][j - 1] + score_match)
                graph[i][j] = max(candidate_scores_list)

    # initialize output sequence
    s_out_1 = ""
    s_out_2 = ""

    i = length_1 
    j = length_2

    # traceback the graph
    while i != 0 or j != 0:
        if i == 0 or graph[i][j] == graph[i][j - 1] + gap_score and j >= 1:
            s_out_1 += "-"
            s_out_2 += s_2[j-1]
            j -= 1

        elif j == 0 or graph[i][j] == graph[i - 1][j] + gap_score and i >= 1:
            s_out_1 += s_1[i-1]
            s_out_2 += "-"
            i -= 1

        else:
            s_out_1 += s_1[i-1]
            s_out_2 += s_2[j-1]
            i -= 1
            j -= 1

    # the result alignment
    s_out_1 = s_out_1[::-1]
    s_out_2 = s_out_2[::-1]

    return (s_out_1, s_out_2)


if __name__ == '__main__':
    print("Put the first sequence")
    seq_1 = input()
    print("Put the second sequence")
    seq_2 = input()

    s_out_1, s_out_2 = global_alignment(seq_1, seq_2)    

    print("\n=========================\n")
    print(s_out_1)
    print(s_out_2)
    print("\n=========================\n")
