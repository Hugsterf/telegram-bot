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
        if (!file.is_open())
        {
            return 0;
        }

        std::string line;
        int line_index = -1;
        int found_index = -1;
        int new_count = 0;

        while (getline(file, line))
        {
            line_index++;
            size_t space_pos = line.find(' ');
            if (space_pos == std::string::npos) continue;

            std::string promo_base = line.substr(0, space_pos);
            int count = std::stoi(line.substr(space_pos + 1));

            if (promo_user == promo_base && count > 0)
            {
                found_index = line_index;
                new_count = count - 1;
                break;
            }
        }
        file.close();

        if (found_index == -1) return 0;

        rework_count(new_count, found_index);
        return 1;
    }

    void rework_count(int countint, int index)
    {
        ifstream count_file(filename);
        if (!count_file.is_open()) return;

        int line_count = 0;
        std::string temp_line;
        while (getline(count_file, temp_line)) line_count++;
        count_file.close();

        std::string* lines = new std::string[line_count];

        ifstream in_file(filename);
        if (!in_file.is_open())
        {
            delete[] lines;
            return;
        }

        for (int i = 0; i < line_count; i++)
        {
            getline(in_file, lines[i]);
        }
        in_file.close();

        if (index >= 0 && index < line_count)
        {
            std::string& line = lines[index];
            size_t space_pos = line.find(' ');
            if (space_pos != std::string::npos)
            {
                std::string promo = line.substr(0, space_pos);
                line = promo + " " + std::to_string(countint);
            }
        }

        ofstream out_file(filename);
        if (!out_file.is_open())
        {
            delete[] lines;
            return;
        }

        for (int i = 0; i < line_count; i++)
        {
            out_file << lines[i] << std::endl;
        }
        out_file.close();

        delete[] lines;
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

    int find_promocode(char* promocode)
    {
        return base.find_promo(std::string(promocode));
    }
}