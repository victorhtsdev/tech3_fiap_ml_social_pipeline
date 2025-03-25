import React, { useState, useEffect } from "react";
import { SidebarContainer, SearchBarWrapper, SearchBar, Divider, MenuWrapper, MenuItem } from "./styles";
import { Search } from "lucide-react";
import { getMenuItems } from "../../services/api";
import ControlPanel from "../ControlPanel/ControlPanel";

const Sidebar = ({ setSelectedItem }) => {
  const [searchTerm, setSearchTerm] = useState("");
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

  const handleSearch = (event) => {
    const query = event.target.value.toLowerCase();
    setSearchTerm(query);
    setLocalSelectedItem(null);

    const filtered = menuItems.filter(item =>
      item.name.toLowerCase().includes(query)
    );

    setFilteredItems(filtered);
  };

  const handleSelect = (item) => {
    setLocalSelectedItem(item);
    setSelectedItem(item);
    setSearchTerm("");
  };

  return (
    <>
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

      <ControlPanel 
        searchTerm={searchTerm} 
        selectedItem={selectedItem} 
        refreshSidebar={fetchData} 
      />
    </>
  );
};

export default Sidebar;
