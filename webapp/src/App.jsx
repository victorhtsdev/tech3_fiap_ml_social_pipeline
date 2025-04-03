import React, { useState, useEffect } from "react";
import Sidebar from "./components/Sidebar/Sidebar";
import ControlPanel from "./components/ControlPanel/ControlPanel";
import AnalysisList from "./components/AnalysisList/AnalysisList";
import CategoryAnalysis from "./components/CategoryAnalysis/CategoryAnalysis";
import ModelExplorerScreen from "./components/ModelExplorerScreen/ModelExplorerScreen";
import { fetchAndStoreToken } from "./services/api";

const App = () => {
  const [selectedItem, setSelectedItem] = useState(null);
  const [selectedAnalysis, setSelectedAnalysis] = useState(null);
  const [reloadAnalysisList, setReloadAnalysisList] = useState(false);
  const [showModelExplorer, setShowModelExplorer] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    fetchAndStoreToken();
  }, []);

  return (
    <div>
      <ControlPanel
        searchTerm={searchTerm}
        selectedItem={selectedItem}
        setReloadAnalysisList={setReloadAnalysisList}
        openModelExplorer={() => setShowModelExplorer(true)}
      />
      <div style={{ display: "flex", marginTop: "50px" }}>
        <Sidebar
          setSelectedItem={setSelectedItem}
          setReloadAnalysisList={setReloadAnalysisList}
          searchTerm={searchTerm}
          setSearchTerm={setSearchTerm}
          reloadAnalysisList={reloadAnalysisList}
          setCurrentScreen={() => {
            setShowModelExplorer(false);
            setSelectedAnalysis(null);
          }}
        />
        <div style={{ flex: 1, padding: "20px", marginLeft: "240px" }}>
          {showModelExplorer ? (
            <ModelExplorerScreen onBack={() => setShowModelExplorer(false)} />
          ) : selectedAnalysis ? (
            <CategoryAnalysis
              execId={selectedAnalysis.id}
              onBack={() => setSelectedAnalysis(null)}
            />
          ) : (
            selectedItem && (
              <AnalysisList
                searchTerm={selectedItem.name}
                onSelectAnalysis={setSelectedAnalysis}
                reloadTrigger={reloadAnalysisList}
              />
            )
          )}
        </div>
      </div>
    </div>
  );
};

export default App;
