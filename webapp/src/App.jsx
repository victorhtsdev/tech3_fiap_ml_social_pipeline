import React, { useState } from "react";
import Sidebar from "./components/Sidebar/Sidebar";
import ControlPanel from "./components/ControlPanel/ControlPanel";
import AnalysisList from "./components/AnalysisList/AnalysisList";
import CategoryAnalysis from "./components/CategoryAnalysis/CategoryAnalysis";

const App = () => {
  const [selectedItem, setSelectedItem] = useState(null);
  const [selectedAnalysis, setSelectedAnalysis] = useState(null);
  const [reloadAnalysisList, setReloadAnalysisList] = useState(false);

  return (
    <div>
      <ControlPanel
        searchTerm={selectedItem?.name || ""}
        selectedItem={selectedItem}
        setReloadAnalysisList={setReloadAnalysisList}
      />
      <div style={{ display: "flex", marginTop: "50px" }}>
        <Sidebar
          setSelectedItem={setSelectedItem}
          setReloadAnalysisList={setReloadAnalysisList}
        />
        <div style={{ flex: 1, padding: "20px", marginLeft: "240px" }}>
          {selectedAnalysis ? (
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
