import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:5000/api",
});

export const getMenuItems = async () => {
  try {
    const response = await api.get("/get_ml_execution_last_version");

    console.log("🔍 Resposta da API:", response.data);

    if (!Array.isArray(response.data)) {
      throw new Error("Resposta da API não é um array.");
    }

    return response.data.map(item => ({
      id: item.id,
      name: item.search || "Nome não disponível",
      date: item.date,
      version: item.version
    }));
  } catch (error) {
    console.error("🚨 Erro ao buscar itens do menu:", error);
    return [];
  }
};

export const runPipeline = async (payload) => {
  try {
    const response = await api.post("/run_pipeline", { search: payload.search }); 
    return response.data;
  } catch (error) {
    console.error("🚨 Erro ao executar o pipeline:", error);
    throw error;
  }
};

export const getPipelineStatus = async (execId) => {
  try {
    const response = await api.get(`/get_pipeline_status?exec_id=${execId}`);
    return response.data;
  } catch (error) {
    console.error("🚨 Erro ao buscar status do pipeline:", error);
    return null;
  }
};

export const getAnalysesBySearch = async (searchTerm) => {
  try {
    const response = await api.get(`/get_ml_executions_by_search?search=${searchTerm}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching analyses:", error);
    return [];
  }
};

export const getSvmCategoryCounts = async (execId) => {
  try {
    const response = await api.get(`/get_svm_category_counts?exec_id=${execId}`);
    return response.data;
  } catch (error) {
    console.error("🚨 Erro ao buscar os dados do SVM:", error);
    return [];
  }
};

export const getWordCloud = async (execId) => {
  try {
    const response = await api.get(`/get_word_cloud?exec_id=${execId}`);
    return response.data;
  } catch (error) {
    console.error("🚨 Erro ao buscar dados da nuvem de palavras:", error);
    throw error;
  }
};

export const getCategoryColors = async (execId) => {
  try {
    const response = await api.get(`/get_category_colors?exec_id=${execId}`);
    return response.data;
  } catch (error) {
    console.error("🚨 Error fetching category colors:", error);
    return {};
  }
};

export default api;

