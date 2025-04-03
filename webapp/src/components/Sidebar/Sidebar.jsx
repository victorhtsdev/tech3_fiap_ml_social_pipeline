import React, { useState, useEffect } from "react";
import {
  SidebarContainer,
  SearchBarWrapper,
  SearchBar,
  Divider,
  MenuWrapper,
  MenuItem
} from "./styles";
import { Search } from "lucide-react";
import { getMenuItems } from "../../services/api";

const Sidebar = ({
  setSelectedItem,
  setReloadAnalysisList,
  searchTerm,
  setSearchTerm,
  reloadAnalysisList,
  setCurrentScreen // ✅ nova prop
}) => {
  const [menuItems, setMenuItems] = useState([]);
  const [filteredItems, setFilteredItems] = useState([]);
  const [selectedItem, setLocalSelectedItem] = useState(null);

  const fetchData = async () => {
    const data = await getMenuItems();
    if (data.length > 0) {
      setMenuItems(data);
      setFilteredItems(data);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    fetchData();
  }, [reloadAnalysisList]);

  const handleSearch = (event) => {
    const query = event.target.value.toLowerCase();
    setSearchTerm(query);
  
    if (query.trim() !== "") {
      setLocalSelectedItem(null);
      setSelectedItem(null); 
    }
  
    const filtered = menuItems.filter(item =>
      item.name.toLowerCase().includes(query)
    );
  
    setFilteredItems(filtered);
  };

  const handleSelect = (item) => {
    setLocalSelectedItem(item);
    setSelectedItem(item);
    setSearchTerm("");
    setCurrentScreen("analysis");
  };

  return (
    <SidebarContainer>
      <SearchBarWrapper>
        <SearchBar>
          <Search size={18} />
          <input
            type="text"
            placeholder="Search terms..."
            value={searchTerm}
            onChange={handleSearch}
          />
        </SearchBar>
      </SearchBarWrapper>

      <Divider />

      <MenuWrapper>
        {filteredItems.length > 0 ? (
          filteredItems.map(item => (
            <MenuItem
              key={item.id}
              className={selectedItem?.id === item.id ? "active" : ""}
              onClick={() => handleSelect(item)}
            >
              {item.name}
            </MenuItem>
          ))
        ) : (
          <p>No terms found.</p>
        )}
      </MenuWrapper>
    </SidebarContainer>
  );
};

export default Sidebar;
