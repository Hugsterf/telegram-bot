#include <iostream>
#include <string>
#include <fstream>

using namespace std;

struct DATABASE
{
    std::string promo;
    std::string filename = "base_promo.txt";

    DATABASE() {};

    int find_promo(std::string promo_user)
    {
        ifstream file(filename);
        if (file.is_open())
        {
            std::string line;
            std::string promo_base;
            std::string count;
            int IndexLine = -1;
            bool flag = false;

            while (getline(file, line))
            {
                IndexLine++;
                for (int i = 0; i < line.size(); i++)
                {
                    if (line[i] == ' ') { flag = true; }
                    else if (flag == false) { promo_base += line[i]; }
                    else { count += line[i]; }
                }
                if (promo_user == promo_base and stoi(count) > 0)
                {
                    int countint = stoi(count);
                    countint--;
                    file.close();
                    rework_count(countint, IndexLine);
                    return 1;

                }
            }
            file.close();
            return 0;
        }
        else
        {
            std::cout << "Error find_promo";
            return 0;
        }
        return 0;
    }

    void rework_count(int countint, int index)
    {
        ifstream file(filename);
        if (file.is_open())
        {
            std::string line;
            int k = 0;
            int j = 0;

            while (getline(file, line)) { k++; }

            std::string* lines = new std::string[k];
            file.clear();
            file.seekg(0);

            while (getline(file, line))
            {
                lines[j] = line;
                j++;
            }
            file.close();

            fstream temp(filename, ios::out | ios::trunc);
            if (temp.is_open())
            {
                for (int i = 0; i < k; i++)
                {
                    if (i == index)
                    {
                        std::string promo_index;
                        std::string count_index;
                        bool flag = false;

                        for (int n = 0; n < lines[i].size(); n++)
                        {
                            if (lines[i][n] == ' ') { flag = true; }
                            else if (flag == false) { promo_index += lines[i][n]; }
                            else { count_index += lines[i][n]; }
                        }

                        temp << promo_index << " " << countint << std::endl;
                    }
                    else
                    {
                        temp << lines[i] << std::endl;
                    }
                }
                temp.close();
            }
            delete[] lines;
        }
    }

    void add_promo(std::string new_promo, int count)
    {
        ofstream file(filename, ios::app);
        if (file.is_open())
        {
            file << new_promo << " " << count << std::endl;
        }
    }
};

extern "C"
{
    DATABASE base;

    void add_promocode(char* promocode, int count)
    {
        base.add_promo(std::string(promocode), int(count));
    }

    void find_promocode(char* promocode)
    {
        base.find_promo(std::string(promocode));
    }
}