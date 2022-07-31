#include <vector>
#include <iostream>
#include <list>

using std::vector;
using std::cin;
using std::cout;
using std::list;
using std::pair;

class lazyprop_segtree{
    vector<int> tree;
    vector<int> lazy_tree;

    public:
    lazyprop_segtree(int size) {
        tree = vector<int>(size*4+1, 0);
        lazy_tree = vector<int>(size*4+1, 0);
    }

    lazyprop_segtree(vector<int>&init_list) {
        int size = init_list.size();
        tree = vector<int>(size*4+1, 0);
        lazy_tree = vector<int>(size*4+1, 0);

        initialize(init_list, 1, size, 1);
    }

    void initialize(vector<int> &init_list, int start, int end, int tree_idx) {
        if (start == end) {
            tree[tree_idx] = init_list[start-1];
        }
        else {
            int mid = (start + end) / 2;
            initialize(init_list, start, mid, tree_idx*2);
            initialize(init_list, mid+1, end, tree_idx*2+1);
            tree[tree_idx] = tree[tree_idx*2] + tree[tree_idx*2+1];
        }
    }

    void lazyprop(int start, int end, int tree_idx) {
        if (lazy_tree[tree_idx] == 0) return ;
        int mid = (start + end) / 2;
        tree[tree_idx] += lazy_tree[tree_idx] * (end -start + 1);
        if (start != end) {
            lazy_tree[tree_idx*2] += lazy_tree[tree_idx];
            lazy_tree[tree_idx*2+1] += lazy_tree[tree_idx];
        }
        lazy_tree[tree_idx] = 0;
    }

    void add(int start, int end, int goal_start, int goal_end, int tree_idx, int val) {
        lazyprop(start, end, tree_idx);
        if (goal_end < start || goal_start > end) {
            return;
        }

        if (goal_start <= start && end <= goal_end) {
            if (start != end) {
                lazy_tree[tree_idx*2] += val;
                lazy_tree[tree_idx*2+1] += val;
            }
            tree[tree_idx] += val * (end -start + 1);
            return;
        }

        int mid = (start + end) / 2;
        add(start, mid, goal_start, goal_end, tree_idx*2, val);
        add(mid+1, end, goal_start, goal_end, tree_idx*2+1, val);
        tree[tree_idx] = tree[tree_idx*2] + tree[tree_idx*2+1];
    }

    int get_sum(int start, int end, int goal_start, int goal_end, int tree_idx) {
        lazyprop(start, end, tree_idx);
        if (goal_end < start || goal_start > end) {
            return 0;
        }

        if (goal_start <= start && end <= goal_end) {
            return tree[tree_idx];
        }

        int mid = (start + end) / 2;
        return get_sum(start, mid, goal_start, goal_end, tree_idx*2) + get_sum(mid+1, end, goal_start, goal_end, tree_idx*2+1);
    }
};

void dfs(vector<list<int>*> &children_ids_from_id, vector<int> &visit_from_id, vector<int> &id_from_visit, vector<pair<int, int>*> &subtree_visits_from_id, int &cur_visit, int cur_id) {
    visit_from_id[cur_id] = cur_visit;
    id_from_visit[cur_visit] = cur_id;
    subtree_visits_from_id[cur_id]->first = cur_visit;

    for (list<int>::iterator it=children_ids_from_id[cur_id]->begin(); it!=children_ids_from_id[cur_id]->end(); it++) {
        cur_visit++;
        dfs(children_ids_from_id, visit_from_id, id_from_visit, subtree_visits_from_id, cur_visit, (*it));
    }

    subtree_visits_from_id[cur_id]->second = cur_visit;
}

int main() {
    int n, m;
    cin >> n >> m;

    vector<int> praises_from_id(n+1, 0);
    vector<int> visit_from_id(n+1, 0);
    vector<int> id_from_visit(n+1, 0);
    vector<list<int>*> children_ids_from_id(n+1, NULL);
    vector<pair<int, int>*> subtree_visits_from_id(n+1, NULL);

    int cur_visit = 1;
    

    lazyprop_segtree segtree(n);

    int parent;
    for (int i=1; i<=n; i++) {
        children_ids_from_id[i] = new list<int>();
        subtree_visits_from_id[i] = new pair<int, int>(0, 0);
    }
    cin >> parent;
    for (int i=2; i<=n; i++) {
        cin >> parent;
        children_ids_from_id[parent]->push_back(i);
    }

    dfs(children_ids_from_id, visit_from_id, id_from_visit, subtree_visits_from_id, cur_visit, 1);

    int query;
    int a, x;

    for (int i=0; i<m; i++) {
        cin >> query;
        if (query == 1) {
            cin >> a >> x;
            segtree.add(1, n, subtree_visits_from_id[a]->first, subtree_visits_from_id[a]->second, 1, x);
        }
        else {
            cin >> a;
            cout << segtree.get_sum(1, n, visit_from_id[a], visit_from_id[a], 1) << "\n";
        }
    }
}