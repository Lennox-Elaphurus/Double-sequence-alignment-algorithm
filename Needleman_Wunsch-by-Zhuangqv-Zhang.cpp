#include <cstdio>
#include <cstring>
#include <cctype>
#include <algorithm>
#define maxlen 100
using namespace std;

int score[256][256], d, DP[maxlen][maxlen], len1, len2;
char S1[maxlen], S2[maxlen], wayY[maxlen], wayX[maxlen];

void Initialization (void) {
    FILE *fin = fopen("BLOSUM-45.txt", "r");
    fscanf(fin, "d=%d%*c", &d);
    int A[maxlen], n = 0, ch, x;
    while ((ch = fgetc(fin)) != '\n')
        if (isalpha(ch)) A[++n] = ch;
    while (fscanf(fin, "%s", &ch) != EOF) {
        for (int i = 1; i <= n; i++) {
            fscanf(fin, "%d", &x);
            score[A[i]][ch] = score[ch][A[i]] = x;
        }
    }
    fclose(fin);
    printf("�Ѵ� BLOSUM-45.txt �������־���\n\n");
}
void Read (void) {
    S1[0] = S2[0] = ' ';
    printf("�������һ��DNA���У�");
    scanf("%s", S1 + 1);
    printf("������ڶ���DNA���У�");
    scanf("%s", S2 + 1);
    len1 = strlen(S1 + 1);
    len2 = strlen(S2 + 1);
}
void Needleman_Wunsch (void) {
    DP[0][0] = 0;
    for (int i = 1; i <= len1; i++) DP[i][0] = -d * i;
    for (int j = 1; j <= len2; j++) DP[0][j] = -d * j;
    for (int i = 1; i <= len1; i++)
        for (int j = 1; j <= len2; j++) {
            DP[i][j] = max(DP[i - 1][j] - d, DP[i][j - 1] - d);
            DP[i][j] = max(DP[i - 1][j - 1] + score[S1[i]][S2[j]], DP[i][j]);
        }
    printf("\nNeedleman-Wunsch�㷨�Ĺ���ͼ���£�\n         ");
    for (int j = 1; j <= len2; j++)
        printf("%8c", S2[j]);
    for (int i = 0; i <= len1; i++) {
        printf("\n%c", S1[i]);
        for (int j = 0; j <= len2; j++)
            printf("%8d", DP[i][j]);
    }
}
void Print (int n) {
    static int num = 0;
    printf("\n\n�� %d ������ƥ�䷽�����£�\n", ++num);
    for (int i = n - 1; i >= 1; i--)
        if(wayY[i + 1] == wayY[i]) printf("-");
        else printf("%c", S1[wayY[i]]);
    printf("\n");
    for (int i = n - 1; i >= 1; i--)
        if(wayX[i + 1] == wayX[i]) printf("-");
        else printf("%c", S2[wayX[i]]);
    printf("\n");
}
void Search (int n, int y, int x) {
    wayY[n] = y;
    wayX[n] = x;
    if (y == 0 && x == 0) {
        Print(n);
        return;
    }
    if(y > 0 && DP[y][x] == DP[y - 1][x] - d)
        Search( n + 1, y - 1, x);
    if(x > 0 && DP[y][x] == DP[y][x - 1] - d)
        Search( n + 1, y, x - 1);
    if(y > 0 && x > 0 && DP[y][x] == DP[y - 1][x - 1] + score[S1[y]][S2[x]])
        Search( n + 1, y - 1, x - 1);
}
main (void) {
    Initialization();
    Read();
    Needleman_Wunsch();
    Search(1, len1, len2);
}
