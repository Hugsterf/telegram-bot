#include <iostream>
#include <cstdint>
#include <string>
#include <fstream>
#include <vector>

bool updateCount(const std::string userpromo, const std::string mainfile, const std::string indexfile);

#pragma pack(push, 1)
struct db
{
	std::string promo;
	int count;

	db() : count(0), promo("") {}

	db(std::string promo, int count)
	{
		this->promo = promo;
		this->count = count;
	}
};
#pragma pack(pop)

void savePromo(const db& db, const std::string mainfile, const std::string indexfile)
{
    std::ofstream filemain(mainfile, std::ios::binary | std::ios::app);
    std::ofstream fileindex(indexfile, std::ios::binary | std::ios::app);
    if (!filemain.is_open() or !fileindex.is_open()) {
        std::cout << "Error save filemain";
        exit(0);
    }

    size_t len = db.promo.size();
    fileindex.write(reinterpret_cast<const char*>(&len), sizeof(len));
    filemain.write(db.promo.c_str(), len);
    filemain.write(reinterpret_cast<const char*>(&db.count), sizeof(db.count));

    filemain.close();
    fileindex.close();
}

void outPromo(const std::string mainfile, const std::string indexfile) 
{
    std::ifstream filemain(mainfile, std::ios::binary);
    std::ifstream fileindex(indexfile, std::ios::binary);
    if (!filemain.is_open() or !fileindex.is_open()) 
    {
        std::cout << "Error save filemain";
        exit(0);
    }

    std::vector<uint64_t> massindex;
    uint64_t len;
    while (fileindex.read(reinterpret_cast<char*>(&len), sizeof(len))) 
    {
        massindex.push_back(len);
    }

    for (uint64_t len : massindex) {
        db user;
        user.promo.resize(len);
        filemain.read(&user.promo[0], len);
        filemain.read(reinterpret_cast<char*>(&user.count), sizeof(user.count));

        std::cout << "Promo: " << user.promo << std::endl;
        std::cout << "Count: " << user.count << std::endl << std::endl;
    }
}

bool findPromo(const std::string userpromo, const std::string mainfile, const std::string indexfile)
{
    std::ifstream filemain(mainfile, std::ios::binary);
    std::ifstream fileindex(indexfile, std::ios::binary);
    if (!filemain.is_open() or !fileindex.is_open()) 
    {
        std::cout << "Error save filemain";
        exit(0);
    }

    std::vector<uint64_t> massindex;
    uint64_t len;
    while (fileindex.read(reinterpret_cast<char*>(&len), sizeof(len)))
    {
        massindex.push_back(len);
    }

    for (uint64_t len : massindex)
    {
        std::string curpromo;
        curpromo.resize(len);
        filemain.read(&curpromo[0], len);

        filemain.seekg(sizeof(int), std::ios::cur);

        if (curpromo == userpromo)
        {
            filemain.close();
            fileindex.close();
            if (updateCount(userpromo, mainfile, indexfile) == false)
            {
                return false;
            }
            return true;
        }
    }
    filemain.close();
    fileindex.close();
    return false;
}

bool updateCount(const std::string userpromo, const std::string mainfile, const std::string indexfile)
{
    std::fstream filemain(mainfile, std::ios::binary | std::ios::in | std::ios::out);
    std::ifstream fileindex(indexfile, std::ios::binary);
    if (!filemain.is_open() or !fileindex.is_open())
    {
        std::cout << "Error save filemain";
        exit(0);
    }

    std::vector<uint64_t> massindex;
    uint64_t len;
    while (fileindex.read(reinterpret_cast<char*>(&len), sizeof(len)))
    {
        massindex.push_back(len);
    }

    uint64_t current_pos = 0;
    for (uint64_t len : massindex)
    {
        std::string curpromo;
        curpromo.resize(len);
        filemain.read(&curpromo[0], len);
        int current_count;
        filemain.read(reinterpret_cast<char*>(&current_count), sizeof(current_count));

        if (curpromo == userpromo)
        {
            if (current_count <= 0)
            {
                return false;
            }
            current_count--;
            filemain.seekp(current_pos + len);
            filemain.write(reinterpret_cast<const char*>(&current_count), sizeof(current_count));
            filemain.close();
            fileindex.close();
            return true;
        }
        current_pos += len + sizeof(int);
    }
    filemain.close();
    fileindex.close();
    return false;
}

extern "C"
{
    __declspec(dllexport) void add_promocode(const char* promocode, int count);
    __declspec(dllexport) int find_promocode(const char* promocode);

    void add_promocode(const char* promocode, int count)
    {
        std::string mainfile = "base.dat";
        std::string indexfile = "index.dat";
        db base(promocode, count);
        savePromo(base, mainfile, indexfile);
    }

    int find_promocode(const char* promocode)
    {
        std::string mainfile = "base.dat";
        std::string indexfile = "index.dat";
        return(findPromo(promocode, mainfile, indexfile)) ? 1 : 0;
    }
}