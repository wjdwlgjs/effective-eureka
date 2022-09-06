#include <iostream>
#include <vector>
#include <list>
#include <cmath>

using std::cin;
using std::cout;
using std::vector;
using std::list;
using std::min;

vector<int> nodes_visit_ids;
vector<int> nodes_which_scc;
vector<list<int>> nodes_out_adjlist;
vector<list<int>> nodes_in_adjlist;
vector<bool> nodes_has_branch;
vector<int> nodes_cash;

vector<list<int>> sccs_containing_nodes;
vector<int> sccs_cash;
vector<bool> sccs_has_branch;
list<int> stack;

int cur_scc = 0;
int cur_visit = 0;

int dfs(int cur_node) {
    if (nodes_which_scc[cur_node] != -1) return 2147483647;
    if (nodes_visit_ids[cur_node] != -1) return nodes_visit_ids[cur_node];

    nodes_visit_ids[cur_node] = cur_visit;
    int return_value = cur_visit;
    cur_visit ++;
    stack.push_back(cur_node);

    for (auto next_node_ptr = nodes_out_adjlist[cur_node].begin(); next_node_ptr != nodes_out_adjlist[cur_node].end(); next_node_ptr++) {
        return_value = min(return_value, dfs((*next_node_ptr)));
    }

    if (return_value == nodes_visit_ids[cur_node]) {
        int temp_node = -1;
        sccs_containing_nodes.push_back(list<int>());
        sccs_cash.push_back(0);
        sccs_has_branch.push_back(false);

        while (temp_node != cur_node) {
            temp_node = stack.back();
            stack.pop_back();

            nodes_which_scc[temp_node] = cur_scc;
            sccs_containing_nodes[cur_scc].push_back(temp_node);
            sccs_cash[cur_scc] += nodes_cash[temp_node];
            sccs_has_branch[cur_scc] = (sccs_has_branch[cur_scc] || nodes_has_branch[temp_node]);

        }

        cur_scc ++;
    }
    return return_value;
}

int main() {
    int n, m;
    cin >> n >> m;

    for (int i = 0; i <= n; i ++) {
        nodes_has_branch.push_back(false);
        nodes_in_adjlist.push_back(list<int>());
        nodes_out_adjlist.push_back(list<int>());
        nodes_visit_ids.push_back(-1);
        nodes_which_scc.push_back(-1);
    }

    int start_node, end_node;
    for (int i = 0; i < m; i ++) {
        cin >> start_node >> end_node;
        nodes_in_adjlist[end_node].push_back(start_node);
        nodes_out_adjlist[start_node].push_back(end_node);
    }

    int input;
    nodes_cash.push_back(0);
    for (int i = 1; i <= n; i++) {
        cin >> input;
        nodes_cash.push_back(input);
    }

    int s, p;
    cin >> s >> p;
    for (int i = 0; i < p; i ++) {
        cin >> input;
        nodes_has_branch[input] = true;
    }

    dfs(s);

    for (int i = cur_scc - 1; i >= 0; i--) {
        int max_prev_cash = 0;

        for (auto scc_node_ptr = sccs_containing_nodes[i].begin(); scc_node_ptr != sccs_containing_nodes[i].end(); scc_node_ptr ++) {
            for (auto prev_node_ptr = nodes_in_adjlist[(*scc_node_ptr)].begin(); prev_node_ptr != nodes_in_adjlist[(*scc_node_ptr)].end(); prev_node_ptr ++) {
                if (nodes_which_scc[(*prev_node_ptr)] != i && nodes_which_scc[(*prev_node_ptr)] != -1 && sccs_cash[nodes_which_scc[(*prev_node_ptr)]] > max_prev_cash) {
                    max_prev_cash = sccs_cash[nodes_which_scc[(*prev_node_ptr)]];
                }
            }
        }

        sccs_cash[i] += max_prev_cash;
    }

    int max_cash = 0;
    for (int i=0; i<cur_scc; i++) {
        if (sccs_has_branch[i] && sccs_cash[i] > max_cash) {
            max_cash = sccs_cash[i];
        }
    }

    cout << max_cash;

}