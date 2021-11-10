#include <iostream>
#include <string>
#include <cstring>
#include <vector>
#include <algorithm>
using namespace std;

//Q1:Tree.Class setList找出别名a/b/...,添加TreeNode*->name

struct TreeNode
{
    string name;
    string flag;             //flag="1":union "app_xxx":表名
    vector<TreeNode *> List; //from+
    vector<string> index;    //select+
    vector<string> where;    //where+
};

class Solution
{
    string s_select;
    string s_from;
    string s_where;

public:
    string getSelect()
    {
        return s_select;
    }
    string getFrom()
    {
        return s_from;
    }
    string getWhere()
    {
        return s_where;
    }
    string getFlag(string s)
    {
        string::iterator s1 = s.begin();
        int n = 0;
        string f = "0";
        while (s1 != s.end())
        {
            if (*s1 == '(')
                n++;
            else if (*s1 == ')')
                n--;
            else if (*s1 == 'u' & n == 0 & (s.end() - s1) > 5)
            {
                string ss = s.substr(s1 - s.begin() - 1, 7);
                if (ss == " union ")
                {
                    f = "1";
                    break;
                }
            }
            s1++;
        }
        if (f == "1")
        {
            s_select = "";
            s_from = s;
            s_where = "";
        }
        else
        {
            int select = s.find(" select ") + 1;
            int from = s.find(" from ") + 1;
            int where = -1;
            s1 = s.begin() + select;
            n = 0;
            while (s1 != s.end())
            {
                if (*s1 == '(')
                    n++;
                else if (*s1 == ')')
                    n--;
                else if (*s1 == 'w' & n == 0 & (s.end() - s1) > 5)
                {
                    string ss = s.substr(s1 - s.begin() - 1, 7);
                    if (ss == " where ")
                    {
                        where = s1 - s.begin();
                        break;
                    }
                }
                s1++;
            }
            if (where == -1)
                where = s.length();
            s_select = s.substr(select + 6, from - select - 6);
            s_from = s.substr(from + 4, where - from - 4);
            if (where + 5 > s.length())
                s_where = "";
            else
                s_where = s.substr(where + 5, s.length() - where - 5);
        }
        return f;
    }
};

class Tree
{
    TreeNode *node;

public:
    void setNode(TreeNode *n)
    {
        node = n;
    }
    TreeNode *getNode()
    {
        return node;
    }
    void setFlag(string f)
    {
        node->flag = f;
    }
    void setList(vector<string> v)
    {
        vector<TreeNode *> v1 = {};
        for (int i = 0; i < v.size(); i++)
        {
            TreeNode *node1 = new TreeNode;
            node1->flag = v[i];
            v1.push_back(node1);
        }
        node->List = v1;
    }
    void setIndex(vector<string> v)
    {
        node->index = v;
    }
    void setWhere(vector<string> v)
    {
        node->where = v;
    }
    vector<string> getList(string s)
    {
        int t = s.find("select");
        if (t == s.npos)
        {
            int kk = s.find(")");
            if (kk == s.npos)
                node->flag = s;
            else
                node->flag = s.substr(0, kk);
            return {};
        }
        else if (node->flag != "1")
        {
            vector<string> v;
            int s1 = 0;
            int n = 0;
            int start = 0;
            while (s1 < s.length())
            {
                if (s.at(s1) == '(')
                    n++;
                else if (s.at(s1) == ')')
                    n--;
                else if (s.at(s1) == 'j' & n == 0 & (s.length() - s1) > 4)
                {
                    if (s.substr(s1 - 1, 6) == " join ")
                    {
                        v.push_back(s.substr(start, s1 - start));
                        start = s1 + 4;
                    }
                }
                s1++;
            }
            v.push_back(s.substr(start, s1 - start));
            return v;
        }
        else
        {
            vector<string> v;
            int s1 = 0;
            int n = 0;
            int start = 0;
            while (s1 < s.length())
            {
                if (s.at(s1) == '(')
                    n++;
                else if (s.at(s1) == ')')
                    n--;
                else if (s.at(s1) == 'u' & n == 0 & (s.length() - s1) > 5)
                {
                    if (s.substr(s1 - 1, 7) == " union ")
                    {
                        v.push_back(s.substr(start, s1 - start));
                        start = s1 + 5;
                    }
                }
                s1++;
            }
            v.push_back(s.substr(start, s1 - start));
            return v;
        }
    }
    vector<string> getIndex(string s)
    {
        vector<string> v;
        string ss = "";
        int n = 0;
        for (int i = 0; i < s.length(); i++)
        {
            if (s[i] == '(')
                n++;
            else if (s[i] == ')')
                n--;
            else if (n == 0 & s[i] == ',')
            {
                v.push_back(ss);
                ss = "";
                continue;
            }
            ss += s[i];
        }
        v.push_back(ss);
        return v;
    }
    vector<string> getWhere(string s)
    {
        return {s};
    }
};

class Test
{
public:
    char *function(char *sql, char *tables)
    {
        Solution S;

        std::string s = std::string(sql);

        vector<TreeNode *> nodes;
        TreeNode *firstNode = new TreeNode;
        firstNode->flag = s;
        nodes.push_back(firstNode);
        Tree T;
        for (int i = 0; i < nodes.size(); i++)
        {
            string flag = S.getFlag(nodes[i]->flag);
            string select = S.getSelect();
            string from = S.getFrom();
            string where = S.getWhere();

            T.setNode(nodes[i]);
            T.setFlag(flag);
            T.setIndex(T.getIndex(select));
            T.setList(T.getList(from));
            T.setWhere(T.getWhere(where));
            TreeNode *node = T.getNode();
            for (int j = 0; j < node->List.size(); j++)
            {
                nodes.push_back(node->List[j]);
            }
        }
        //遍历nodes数组,List为空的是根节点,记录其flag
        for (int i = 0; i < nodes.size(); i++)
        {
            if (nodes[i]->List.size() > 0)
                continue;
            else
            {
                strcat(tables, "+");
                strcat(tables, nodes[i]->flag.c_str());
            }
            // tables = tables + "+" + nodes[i]->flag;
        }

        return tables;
    }
};

int main()
{
    Test t;
    char *s = (char *)"";
    char tables[1000];
    // char *ans = (char *)(std::string("  ")).c_str();
    cout << t.function(s, tables) << endl;
}

// extern "C"
// {
//     Test *test_new()
//     {
//         return new Test;
//     }
//     char *main1(Test *t, char *ss)
//     {
//         char *tables = new char[1000];
//         try
//         {
//             return t->function(ss, tables);
//         }
//         catch (exception e)
//         {
//             return "wrong";
//         }
//     }
// }
