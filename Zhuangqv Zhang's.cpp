#include <cstdio>
#include <cstring>
#include <cctype>
#include <algorithm>
#define maxlen 100
using namespace std;

int score[256][256], D, dp[maxlen][maxlen], len1, len2;
char dna1[maxlen], dna2[maxlen], wayY[maxlen], wayX[maxlen];

void Initialization (void) {
    FILE *fin = fopen("BLOSUM-45.txt", "r");
    fscanf(fin, "d=%d%*c", &D);
    int A[maxlen], n = 0, ch = 0, x;
    while (ch != '\n') {
        if (isalpha(ch)) A[++n] = ch;
        ch = fgetc(fin);
    }
    while (fscanf(fin, "%s", &ch) != EOF) {
        for (int i = 1; i <= n; i++) {
            fscanf(fin, "%d", &x);
            score[A[i]][ch] = score[ch][A[i]] = x;
        }
    }
    fclose(fin);
    printf("已从 BLOSUM-45.txt 导入评分矩阵。\n\n");
}
void Read (void) {
    printf("请输入第一条DNA序列：");
    scanf("%s", dna1 + 1);
    printf("请输入第二条DNA序列：");
    scanf("%s", dna2 + 1);
    len1 = strlen(dna1 + 1);
    len2 = strlen(dna2 + 1);
}
void Needleman_Wunsch (void) {
    dp[0][0] = 0;
    for (int i = 1; i <= len1; i++) dp[i][0] = (-D) * i;
    for (int j = 1; j <= len2; j++) dp[0][j] = (-D) * j;
    for (int i = 1; i <= len1; i++)
        for (int j = 1; j <= len2; j++) {
            dp[i][j] = max(dp[i - 1][j] - D, dp[i][j - 1] - D);
            dp[i][j] = max(dp[i - 1][j - 1] + score[dna1[i]][dna2[j]], dp[i][j]);
        }
    printf("\nNeedleman-Wunsch算法的过程图如下：\n         ");
    for (int j = 1; j <= len2; j++)
        printf("%8c", dna2[j]);
    for (int i = 0; i <= len1; i++) {
        printf("\n%c", dna1[i]);
        for (int j = 0; j <= len2; j++)
            printf("%8d", dp[i][j]);
    }
}
void Print (int n) {
    static int num = 0;
    printf("\n\n第 %d 种最优匹配方案如下：\n", ++num);
    for (int i = n - 1; i >= 1; i--)
        if(wayY[i + 1] == wayY[i]) printf("-");
        else printf("%c", dna1[wayY[i]]);
    printf("\n");
    for (int i = n - 1; i >= 1; i--)
        if(wayX[i + 1] == wayX[i]) printf("-");
        else printf("%c", dna2[wayX[i]]);
    printf("\n");
}
void Search (int n, int y, int x) {
    wayY[n] = y;
    wayX[n] = x;
    if (y == 0 && x == 0) {
        Print(n);
        return;
    }
    if(dp[y][x] == dp[y - 1][x] - D)
        Search( n + 1, y - 1, x);
    if(dp[y][x] == dp[y][x - 1] - D)
        Search( n + 1, y, x - 1);
    if(dp[y][x] == dp[y - 1][x - 1] + score[dna1[y]][dna2[x]])
        Search( n + 1, y - 1, x - 1);
}
main (void) {
    Initialization();
    Read();
    Needleman_Wunsch();
    Search(1, len1, len2);
}
