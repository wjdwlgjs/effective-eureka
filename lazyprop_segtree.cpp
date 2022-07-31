#include <vector>

using std::vector;

class lazyprop_segtree{
    vector<long long> tree;
    vector<long long> lazy_tree;

    public:
    lazyprop_segtree(int size) {
        tree = vector<long long>(size*4+1, 0);
        lazy_tree = vector<long long>(size*4+1, 0);
    }

    lazyprop_segtree(vector<long long>&init_list) {
        int size = init_list.size();
        tree = vector<long long>(size*4+1, 0);
        lazy_tree = vector<long long>(size*4+1, 0);

        initialize(init_list, 1, size, 1);
    }

    void initialize(vector<long long> &init_list, int start, int end, int tree_idx) {
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

    void add(int start, int end, int goal_start, int goal_end, int tree_idx, long long val) {
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

    long long get_sum(int start, int end, int goal_start, int goal_end, int tree_idx) {
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
