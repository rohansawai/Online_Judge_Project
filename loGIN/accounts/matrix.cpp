#include <bits/stdc++.h>
using namespace std;

int main(){
    int n, m, q;
    vector<vector<int>> mat(n, vector<int> (m));
    for(int i = 0; i<n; i++){
        for(int j = 0; j<m; j++){
            int x;
            cin>>x;
            mat[i][j] = x;
        }
    }

    for(int i = 0; i<q; i++){
        int x;
        cin>>x;
        int l = 0, r = n*m - 1;

        while(l<r){
            int mid = l + (r-l)/2;

            if(mat[mid/m][mid%m] == x){
                cout<<mid/m<<" "<<mid%m<<"\n";
            }
            else if(mat[mid/m][mid%m] > x){
                r = mid-1;
            }
            else{
                l = mid+1;
            }
        }
    }
}